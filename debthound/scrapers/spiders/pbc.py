import scrapy
import json
import re
import string
import logging

from cryptography.x509 import name
from collections import defaultdict
from urllib.parse import urlencode
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from scrapy.utils.response import open_in_browser

from scrapers.items import PBCPublicRecord
from scrapers.spiders.base import MyBaseSpider


doctypes = ['JUD C', 'D', 'SAT']


def get_form_data(search_entry, from_date, to_date):
    return {
        'search_by': 'DocType',
        'search_entry': '{0}'.format(search_entry),
        'consideration': '&FromDate={0}&ToDate={1}'.format(
            from_date.strftime('%m/%d/%Y'),
            to_date.strftime('%m/%d/%Y')
        ),
        'RecSetSize': '2000',
        'PageSize': '1000'
    }


class PBC(MyBaseSpider):
    name = 'pbc'
    start_urls = ['http://oris.co.palm-beach.fl.us/or_web1/new_sch.asp']
    id = 'http://oris.co.palm-beach.fl.us'

    # todo persist a scrape log by portal address and lookup the desired start date
    init_start_date = date.today() - relativedelta(years=10)
    init_days_increment = 7
    page_size = 2000

    def __init__(self, *args, **kwargs):
        super(PBC, self).__init__(*args, **kwargs)
        assert kwargs.get('mysql_url')
        self.mysql_url = kwargs.get('mysql_url')
        self.doctypes = [kwargs['doctypes']] if kwargs.get('doctypes', None) else doctypes
        self._days_increment = relativedelta(days=self.init_days_increment)
        if 'start_date' in kwargs:
            self._from_date = datetime.strptime(kwargs['start_date'],
                                                '%m/%d/%Y').date()
        else:
            self._from_date = self.init_start_date

        if 'end_date' in kwargs:
            self._max_date = datetime.strptime(kwargs['end_date'],
                                              '%m/%d/%Y').date()
        else:
            self._max_date = self._from_date + self._days_increment

        if self._from_date + self._days_increment <= self._max_date:
            self._to_date = self._from_date + self._days_increment
        else:
            self._to_date = self._max_date

        self._max_date = self._max_date if self._max_date <= date.today() else date.today()
        assert self._from_date < self._to_date

    def start_requests(self):
        print('starting requests')
        for d_type in self.doctypes:
            self._keys[d_type] = set()
            print('type={0}, start={1}, end={2}'.format(d_type, self._from_date, self._max_date))
            yield self.make_doctype_request(d_type, self._from_date, self._to_date)

    def make_doctype_request(self, doctype, from_date, to_date):
        form_data = get_form_data(doctype, from_date, to_date)
        data = urlencode(form_data, safe='&=')
        meta = {
            'from_date': from_date,
            'to_date': to_date,
            'doctype': doctype
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        return scrapy.Request(url=self.start_urls[0],
                              method='POST',
                              body=data,
                              headers=headers,
                              callback=self.parse,
                              meta=meta)

    def parse(self, response):
        overflowtxt = "This search returned over 2000 records."
        overflow = len(
            response.xpath(
                '(//table)[6]//td/strong[contains(.,$of)]',
                of=overflowtxt)) > 0
        paging = response.xpath('//html/body/form/*/form/table/strong//a[contains(., "Next")]')

        # if there are more than 2000 records we have to narrow the search results
        old_meta = response.meta
        info = 'doc_type={0}, from_date={1}, to_date={2}'.format(old_meta['doctype'], old_meta['from_date'],
                                                                 old_meta['to_date'])
        if overflow and old_meta['from_date'] != old_meta['to_date']:
            print("overflow with {0}".format(info))
            logging.getLogger().info("overflow with {0}".format(info))
            from_date = old_meta['from_date']
            to_date = self._increment_days(old_meta['to_date'], -1)
            yield self.make_doctype_request(old_meta['doctype'], from_date, to_date)
        else:

            if old_meta['to_date'] == old_meta['from_date'] and overflow:
                logging.getLogger().error("Over 2000 records for this request: {0}".format(info))
                print("Over 2000 records for this request:", info)

            self.crawler.stats.set_value('{0}__request_info__'.format(self.id), info)
            tpath = '//html/body/form//table[1]/table[2]/tr' if overflow else '//html/body/form//table[2]/tr'
            recs = response.xpath(tpath)
            info = '{0} rec_count={1}'.format(len(recs), info)
            m = "scraping page for {0}".format(info)
            print(m)
            logging.getLogger().info(m)

            for row in recs[1:]:
                if len(row.xpath('td')) == 1:
                    continue
                cfn = row.xpath('./td[8]//text()').extract_first().replace(u'\xa0', u'')
                type_ = row.xpath('./td[5]//text()').extract_first().replace(u'\xa0', u'')
                if self.check_key(type_, cfn):
                    continue
                item = PBCPublicRecord(
                    name=row.xpath('./td[2]//text()').extract_first().replace(u'\xa0', u''),
                    cross_name=row.xpath('./td[3]//text()').extract_first().replace(u'\xa0', u''),
                    date=row.xpath('./td[4]//text()').extract_first().replace(u'\xa0', u''),
                    type_=type_,
                    book=row.xpath('./td[6]//text()').extract_first().replace(u'\xa0', u''),
                    page=row.xpath('./td[7]//text()').extract_first().replace(u'\xa0', u''),
                    cfn=cfn,
                    legal=row.xpath('./td[9]//text()').extract_first().replace(u'\xa0', u''),
                    info=info
                )
                # get the detail
                d_link = row.xpath('./td[1]//@href').extract_first()
                d_link = d_link.replace('\r\n\t\t\t\t\t\t','')
                meta = response.meta
                meta['item'] = item
                yield response.follow(d_link, callback=self.parse_details, meta=meta)

            if len(paging) == 1:
                m = "next page for {0}".format(info)
                print(m)
                logging.getLogger().debug(m)
                link = paging.xpath('./@href').extract_first()
                yield response.follow(link, callback=self.parse, meta=old_meta)
            else:
                # go to next date range search
                self._keys[old_meta['doctype']].clear()
                from_date = old_meta['from_date']
                from_date += old_meta['to_date'] - from_date
                from_date = self._increment_days(from_date, 1)
                to_date = from_date + self._days_increment
                info = 'doc_type={0}, from_date={1}, to_date={2}'.format(old_meta['doctype'],
                                                                         from_date,
                                                                         to_date)
                print("next date range search for:{0}".format(info))

                if from_date < self._max_date:
                    if to_date > self._max_date:
                        info = 'doc_type={0}, from_date={1}, to_date={2}'.format(old_meta['doctype'],
                                                                                 from_date,
                                                                                 to_date)
                        print("to_date: > maxdate: for {0} ; Maxdate is {1}".format(info, self._max_date))
                        to_date = self._max_date
                    yield self.make_doctype_request(
                        doctype=old_meta['doctype'],
                        from_date=from_date,
                        to_date=to_date)
                else:
                    m = ("ended search with {0}".format(info))
                    print(m)
                    logging.getLogger().info(m)

    def parse_details(self, response):
        frame1 = response.xpath('//frame[1]/@src').extract_first()
        if frame1:
            meta = response.meta
            yield response.follow(frame1, self.parse_details, meta=meta)

        else:
            url = response.xpath('//map[@name="get_image"]/area/@href').extract_first()
            url = response.urljoin(url)
            pages = response.xpath('(//table)[5]/tr[6]/td[2]/text()').extract_first()
            consideration = response.xpath('(//table)[5]/tr[7]/td[2]/text()').extract_first()
            consideration = float(re.sub(r'[\$,]', '', consideration))
            party1 = response.xpath('(//table)[5]/tr/td[text()="Party 1:"]/following-sibling::td//dt/text()').extract()
            party2 = response.xpath('(//table)[5]/tr/td[text()="Party 2:"]/following-sibling::td//dt/text()').extract()
            book_type = response.xpath('(//table)[5]/tr/td[text()="Book Type:"]/following-sibling::td/text()').extract_first()
            item = response.meta['item']
            item['pages'] = pages
            item['consideration'] = consideration
            item['party1'] = [re.sub(r'[\r\n\t]', '', s).strip() for s in party1]
            item['party2'] = [re.sub(r'[\r\n\t]', '', s).strip() for s in party2]
            item['image_uri'] = url
            item['book_type'] = book_type
            yield item



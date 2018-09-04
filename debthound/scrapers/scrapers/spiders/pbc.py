import scrapy
import json
import re
import string
import logging

from cryptography.x509 import name
from requests_toolbelt.utils import formdata
from urllib.parse import urlencode
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from scrapy.utils.response import open_in_browser

from scrapers.items import PBCPublicRecord

doctypes = ['D', 'JUD, JUD C']


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


class PBC(scrapy.Spider):
    name = 'pbc'
    start_urls = ['http://oris.co.palm-beach.fl.us/or_web1/new_sch.asp']

    # todo persist a scrape log by portal address and lookup the desired start date
    init_start_date = date.today() - relativedelta(years=10)
    init_days_increment = 7
    page_size = 2000

    def __init__(self, *args, **kwargs):
        super(PBC, self).__init__()
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

        assert self._max_date <= date.today()
        assert self._from_date < self._to_date

    @staticmethod
    def _increment_days(begin_date, days):
        return begin_date + relativedelta(days=days)

    def start_requests(self):
        for d_type in doctypes:
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
        if overflow:
            from_date = old_meta['from_date']
            to_date = self._increment_days(old_meta['to_date'], -1)
            yield self.make_doctype_request(old_meta['doctype'], from_date, to_date)
        else:
            for row in response.xpath('//html/body/form//table[2]/tr')[1:]:
                item = PBCPublicRecord(
                    name=row.xpath('./td[2]//text()').extract_first().replace(u'\xa0', u''),
                    cross_name=row.xpath('./td[3]//text()').extract_first().replace(u'\xa0', u''),
                    date=row.xpath('./td[4]//text()').extract_first().replace(u'\xa0', u''),
                    type_=row.xpath('./td[5]//text()').extract_first().replace(u'\xa0', u''),
                    book=row.xpath('./td[6]//text()').extract_first().replace(u'\xa0', u''),
                    page=row.xpath('./td[7]//text()').extract_first().replace(u'\xa0', u''),
                    cfn=row.xpath('./td[8]//text()').extract_first().replace(u'\xa0', u''),
                    legal=row.xpath('./td[9]//text()').extract_first().replace(u'\xa0', u'')
                )
                # get the detail
                d_link = row.xpath('./td[1]//@href').extract_first()
                d_link = d_link.replace('\r\n\t\t\t\t\t\t','')
                meta = response.meta
                meta['item'] = item
                yield response.follow(d_link, callback=self.parse_details, meta=meta)

            if len(paging) == 1:
                link = paging.xpath('./@href').extract_first()
                yield response.follow(link, callback=self.parse, meta=old_meta)
            else:
                # go to next date range search
                from_date = old_meta['from_date']
                from_date += old_meta['to_date'] - from_date
                to_date = from_date + self._days_increment

                if from_date < self._max_date:
                    if to_date > self._max_date:
                        to_date = self._max_date
                    yield self.make_doctype_request(
                        doctype=old_meta['doctype'],
                        from_date=from_date,
                        to_date=to_date)

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
            # todo: get image url
            item = response.meta['item']
            item['pages'] = pages
            item['consideration'] = consideration
            item['party1'] = [re.sub(r'[\r\n\t]', '', s).strip() for s in party1]
            item['party2'] = [re.sub(r'[\r\n\t]', '', s).strip() for s in party2]
            item['image_uri'] = url
            item['book_type'] = book_type
            yield item
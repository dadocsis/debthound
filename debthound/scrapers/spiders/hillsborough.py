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


def get_url_qs(url, search_entry, from_date, to_date, current_date):
    params = {
        'bd': from_date.strftime('%m/%d/%Y'),
        'ed': to_date.strftime('%m/%d/%Y'),
        'bt': 'O',
        'd': current_date.strftime('%m/%d/%Y'),
        'pt': -1,
        'dt': search_entry,
        'st': 'documenttype'
    }
    return f"{url}?{urlencode(params, safe='&=')}"


class Hillsborough(MyBaseSpider):
    _doctypes = ['CCJ', 'D', 'SAT']
    name = 'hillsborough'
    start_urls = ['http://pubrec3.hillsclerk.com/oncore/search.aspx']
    id = 'http://pubrec3.hillsclerk.com'
    _doctype_maps = {
        'DEED': 'D',
        'SATISFACTION': 'SAT',
        'CERTIFIED COPY OF A COURT JUDGMENT': 'JUD C'
    }

    # todo persist a scrape log by portal address and lookup the desired start date
    init_start_date = date.today() - relativedelta(years=10)
    init_days_increment = 7
    page_size = 2000

    def start_requests(self):
        print('starting requests')
        for d_type in self.doctypes:
            self._keys[d_type] = set()
            print('type={0}, start={1}, end={2}'.format(d_type, self._from_date, self._max_date))
            yield self.make_doctype_request(d_type, self._from_date, self._to_date, date.today(), True)

    def make_doctype_request(self, doctype, from_date, to_date, today, merge_cookies=False, session=None):
        meta = {
            'from_date': from_date,
            'to_date': to_date,
            'doctype': doctype,
            'dont_merge_cookies': not merge_cookies,
            'session': session
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        if session:
            headers['Cookie'] = f'ASP.NET_SessionId={session}'
        url = get_url_qs(self.start_urls[0], doctype, from_date, to_date, today)
        return scrapy.Request(url=url,
                              method='POST',
                              headers=headers,
                              callback=self.parse,
                              meta=meta)

    def parse(self, response):
        overflow = response.xpath('//*[@id="trExceedMessage"]//text()').get().strip()
        old_meta = response.meta
        info = 'doc_type={0}, from_date={1}, to_date={2}'.format(old_meta['doctype'], old_meta['from_date'],
                                                                 old_meta['to_date'])
        session = (old_meta.get('session') or
                   response.headers.getlist('Set-Cookie')[0].decode().split('=')[1].split(";")[0])

        if overflow and old_meta['from_date'] != old_meta['to_date']:
            #print("overflow with {0}".format(info))
            logging.getLogger().info("overflow with {0}".format(info))
            from_date = old_meta['from_date']
            to_date = self._increment_days(old_meta['to_date'], -1)
            yield self.make_doctype_request(old_meta['doctype'], from_date, to_date, date.today())
        else:
            if old_meta['to_date'] == old_meta['from_date'] and overflow:
                logging.getLogger().error("Over 2000 records for this request: {0}".format(info))
                #print("Over 2000 records for this request:", info)

            self.crawler.stats.set_value('{0}__request_info__'.format(self.id), info)
            tpath = '//*[@id="dgResults"]//tr'
            recs = response.xpath(tpath)

            if recs:
                pager_row = recs[-1]
                page_number = pager_row.xpath('./td[1]//span//text()').get().strip()
                logging.getLogger().info(f'Scraping {len(recs[2:-1])} records on page {page_number} for: {info}')
                for row in recs[2:-1]:
                    doctype = row.xpath('./td[6]//text()').extract_first().strip()
                    cfn = row.xpath('./td[10]//text()').extract_first().strip()
                    if self.check_key(doctype, cfn):
                        continue
                    try:
                        item = self.create_item(row, doctype, cfn, info)
                        yield item
                    except Exception as ex:
                        logging.getLogger().error(f"Unable to create item {row}")
                        continue
                paging = pager_row.xpath('./td[1]//a')  # if there are anchors in the paging row we have multiple pages
                next_page = pager_row.xpath('./td//span/following-sibling::a[1]')
                if paging and next_page:
                    logging.getLogger().info(f'moving to page {int(page_number)+1} for {info}')
                    s = next_page.attrib['href']  # "javascript:__doPostBack('dgResults$ctl34$ctl01','')"
                    m = re.search(r'dgResults(\$[\w\d]+){2}', s)
                    vsg = response.xpath('//*[@id="__VIEWSTATEGENERATOR"]').attrib['value']
                    ev = response.xpath('//*[@id="__EVENTVALIDATION"]').attrib['value']
                    vs = response.xpath('//*[@id="__VIEWSTATE"]').attrib['value']
                    paging_form_data = {
                        '__EVENTTARGET': m[0],
                        '__VIEWSTATEGENERATOR': vsg,
                        '__EVENTVALIDATION': ev,
                        '__VIEWSTATE': vs
                    }
                    old_meta['dont_merge_cookies'] = True
                    old_meta['session'] = session
                    yield response.request.replace(
                        body=urlencode(paging_form_data, safe='&='), meta=old_meta,
                        headers={'Content-Type': 'application/x-www-form-urlencoded',
                                 'Cookie': f'ASP.NET_SessionId={session}'})
                else:
                    print('go to next date range')
                    yield self.go_to_next_date_range(old_meta, session)

            else:
                logging.getLogger().info(f'no records where found for the the following: {info}')
                yield self.go_to_next_date_range(old_meta, session)

            # go to next date range search
            # self._keys[old_meta['doctype']].clear()
            # from_date = old_meta['from_date']
            # from_date += old_meta['to_date'] - from_date
            # from_date = self._increment_days(from_date, 1)
            # to_date = from_date + self._days_increment
            # info = 'doc_type={0}, from_date={1}, to_date={2}'.format(old_meta['doctype'], from_date, to_date)
            # logging.getLogger().info("next date range search for:{0}".format(info))
            #
            # if from_date < self._max_date:
            #     if to_date > self._max_date:
            #         info = 'doc_type={0}, from_date={1}, to_date={2}'.format(old_meta['doctype'],
            #                                                                  from_date,
            #                                                                  to_date)
            #         logging.getLogger().info("to_date: > maxdate: for {0} ; Maxdate is {1}".format(info, self._max_date))
            #         to_date = self._max_date
            #
            #     yield self.make_doctype_request(doctype=old_meta['doctype'], from_date=from_date,
            #                                     to_date=to_date, today=date.today(), session=session)
            # else:
            #     logging.getLogger().info(f"ended search with {info}")

    def create_item(self, row, doctype, cfn, info):
        url = row.xpath('./td[3]/a/@href').extract_first()
        party1 = cross_name = row.xpath('./td[3]/a/text()').extract_first().strip()
        party2 = row.xpath('./td[4]//text()').extract_first().strip()
        _date = row.xpath('./td[5]//text()').extract_first().strip()
        doctype = doctype
        book = row.xpath('./td[7]//text()').extract_first().strip()
        page = row.xpath('./td[8]//text()').extract_first().strip()
        legal = row.xpath('./td[9]//text()').extract_first().strip()
        cfn = cfn

        item = PBCPublicRecord(
            name=party1,
            cross_name=cross_name,
            party1=party1,
            party2=party2,
            date=_date,
            type_=self._doctype_maps[doctype],
            book=book,
            page=page,
            legal=legal,
            cfn=cfn,
            info=info,
            image_uri=url,
            book_type=None,
            consideration=0)
        return item

    def go_to_next_date_range(self, old_meta, session):
        # go to next date range search
            self._keys[old_meta['doctype']].clear()
            from_date = old_meta['from_date']
            from_date += old_meta['to_date'] - from_date
            from_date = self._increment_days(from_date, 1)
            to_date = from_date + self._days_increment
            info = 'doc_type={0}, from_date={1}, to_date={2}'.format(old_meta['doctype'], from_date, to_date)
            logging.getLogger().info("next date range search for:{0}".format(info))

            if from_date < self._max_date:
                if to_date > self._max_date:
                    info = 'doc_type={0}, from_date={1}, to_date={2}'.format(old_meta['doctype'],
                                                                             from_date,
                                                                             to_date)
                    logging.getLogger().info("to_date: > maxdate: for {0} ; Maxdate is {1}".format(info, self._max_date))
                    to_date = self._max_date

                return self.make_doctype_request(doctype=old_meta['doctype'], from_date=from_date,
                                                to_date=to_date, today=date.today(), session=session)
            else:
                logging.getLogger().info(f"ended search with {info}")
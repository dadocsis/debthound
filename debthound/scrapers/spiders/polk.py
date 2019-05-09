import json
from urllib.parse import urlencode
from datetime import datetime

import scrapy
import logging

from scrapers.spiders.base import MyBaseSpider
from scrapers.items import PBCPublicRecord


def get_form_data(doc_type, from_date, to_date):
    return {
        'DocTypes': doc_type,
        'FromDate': from_date.strftime('%Y%m%d'),
        'ToDate': to_date.strftime('%Y%m%d'),
        'MaxRows': 5000,
        'StartRow': 0,
        'RowsPerPage': 0
    }


class Polk(MyBaseSpider):
    name = 'polk'
    start_urls = ['https://apps.polkcountyclerk.net/browserviewor/api/search']
    id = 'https://apps.polkcountyclerk.net'

    init_days_increment = 7
    page_size = 10000

    _doctypes = ['CCJ', 'DEED', 'S JDG']
    _doctype_maps = {
        'CCJ': 'JUD C',
        'DEED': 'D',
        'S JDG': 'SAT'
    }

    def make_doctype_request(self, doctype, from_date, to_date):
        data = get_form_data(doctype, from_date, to_date)
        meta = {
            'from_date': from_date,
            'to_date': to_date,
            'doctype': doctype
        }
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://apps.polkcountyclerk.net',
            'Referer': 'https://apps.polkcountyclerk.net/browserviewor/',
            'Accept': 'application/json, text/plain, */*'
        }
        return scrapy.Request(url=self.start_urls[0],
                              method='POST',
                              body=json.dumps(data),
                              headers=headers,
                              callback=self.parse,
                              meta=meta)

    def parse_details(self, response):
        meta = response.meta
        d = json.loads(response.body_as_unicode())
        rdate = datetime.strptime(d['rec_date'], '%Y-%m-%dT%H:%M:%S')
        try:
            item = PBCPublicRecord(
                party1=' '.join([d for d in d['direct_parties']]),
                party2=' '.join([d for d in d['reverse_parties']]),
                name=meta['name'], #meta
                cross_name=d['ret_name'],
                date=rdate.date().strftime('%m/%d/%Y'),
                type_=self._doctype_maps[d['type']],
                book=str(d.get('book', '')),
                book_type=d.get('book_type'),
                page=str(d['page']),
                pages=d.get('doc_pages', 0),
                cfn=d['file_num'],
                legal=d.get('legal_1'),
                info=meta['info'], #meta
                image_uri=str(d['id']),
                consideration=d.get('consid_1', 0) or 0
            )
            yield item
        except Exception as ex:
            logging.getLogger().exception("error creating item: {0}".format(d))

    def start_requests(self):
        print('starting requests')
        for d_type in self.doctypes:
            self._keys[d_type] = set()
            print('type={0}, start={1}, end={2}'.format(d_type, self._from_date, self._max_date))
            yield self.make_doctype_request(d_type, self._from_date, self._to_date)

    def parse(self, response):
        rows = json.loads(response.body_as_unicode())
        if rows:
            info_row = rows[0:1][0]
            rows = rows[1:]
            overflow = info_row['_total_rows'] > info_row['_max_rows']
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
                    logging.getLogger().error("Over {0} records for this request: {1}".format(info_row['_max_rows'], info))
                    print("Over {0} records for this request:".format(info_row['_max_rows']), info)

                self.crawler.stats.set_value('{0}__request_info__'.format(self.id), info)
                info = '{0} rec_count={1}'.format(info, str(len(rows)))
                m = "scraping page for {0}".format(info)
                print(m)
                logging.getLogger().info(m)

                for d in rows:
                    details_url = 'https://apps.polkcountyclerk.net/browserviewor/api/document'
                    params = {"ID": d['doc_id']}
                    meta = {"info": info, "name": d.get('party_name')}
                    yield scrapy.Request(details_url, callback=self.parse_details, method='POST',
                                          headers={'Content-Type': 'application/json', 'Accept': 'application/json, text/plain, */*'},
                                          body=json.dumps(params), meta=meta)


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

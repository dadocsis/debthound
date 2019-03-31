import scrapy
import json
import re
import math
import logging
import requests

from urllib.parse import urlencode
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from scrapy.utils.response import open_in_browser
from scrapy import signals

from scrapers.items import PBCPublicRecord
from scrapers.mylogging import LogToMyDBHandler
from scrapers.spiders.base import MyBaseSpider





def get_form_data(doc_type, from_date, to_date):
    return {
        'DocTypes': doc_type,
        'RecordDateFrom': from_date.strftime('%m/%d/%Y'),
        'RecordDateTo': to_date.strftime('%m/%d/%Y'),
        'X-Requested-With': 'XMLHttpRequest'
    }


class Broward(MyBaseSpider):
    name = 'broward'
    start_urls = ['https://officialrecords.broward.org/AcclaimWeb/search/SearchTypeDocType?Length=6']
    disclaimer = 'https://officialrecords.broward.org/AcclaimWeb/search/Disclaimer'
    grid_results = 'https://officialrecords.broward.org/AcclaimWeb/Search/GridResults'
    has_results = 'https://officialrecords.broward.org/AcclaimWeb/Search/HasResults'
    id = 'https://officialrecords.broward.org'
    image_url = 'https://officialrecords.broward.org/AcclaimWeb/Image/DocumentPdfAllPages/'
    _doctypes = '138, 168, 120'
    # 168 = CERTIFIED FINAL JUDGMENT (CFJ)
    # 138 = DEED TRANSFERS OF REAL PROPERTY (D)
    # 120 = RELEASE/REVOKE/SATISFY OR TERMINATE (RST)
    # 121 = RELEASE/REVOKE/SATISFY OR TERMINATE HIDDEN FROM WEB (RSTX)
    _doctype_maps = {
        'Certified Final Judgment': '168',
        'Deed Transfers of Real Property': '138',
        'Release/Revoke/Satisfy or Terminate': '120'
    }

    init_days_increment = 14
    page_size = 10000

    def __init__(self, *args, **kwargs):
        super(Broward, self).__init__(*args, **kwargs)
        assert kwargs.get('mysql_url')
        self.mysql_url = kwargs.get('mysql_url')
        self.doctypes = [kwargs['doctypes']] if kwargs.get('doctypes', None) else self._doctypes
        self._days_increment = relativedelta(days=self.init_days_increment)
        self._from_date = datetime.strptime(kwargs['start_date'], '%m/%d/%Y').date()
        self._max_date = datetime.strptime(kwargs['end_date'], '%m/%d/%Y').date()

        if self._from_date + self._days_increment <= self._max_date:
            self._to_date = self._from_date + self._days_increment
        else:
            self._to_date = self._max_date

        self._max_date = self._max_date if self._max_date <= date.today() else date.today()
        assert self._from_date < self._to_date
        self.session = None
        self.log_id = None # this gets set in the logging extension

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(Broward, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.setup_custom_logging, signal=signals.engine_started)
        return spider

    def setup_custom_logging(self):
        # Where are doing some custom logging b/c we lose the default logging functionality from doing request nonasync
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        hndlr = LogToMyDBHandler(self.mysql_url, self.log_id)
        hndlr.setLevel(logging.INFO)
        root_logger.addHandler(hndlr)

    def start_requests(self):
        print('getting a session')
        print("accept disclaimer")
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        yield scrapy.Request(self.disclaimer,
                             callback=self.save_session,
                             headers=headers,
                             method='POST', body=urlencode({'disclaimer': 'true'}, safe='&='))

    def save_session(self, response):
        print('save session')
        dotnet_sess = response.request.headers.getlist('Cookie')[0].decode().split('=')
        self.session = {dotnet_sess[0]: dotnet_sess[1]}
        return self.start_doc_scrape(self._from_date, self._to_date)

    def start_doc_scrape(self, from_date, to_date):
        print('starting requests')
        logging.getLogger().warning('starting requests',
                                    extra={'info': 'from_date={0}, to_date={1}'.format(from_date, to_date)})
        r_date_ex = re.compile(r'/Date\((\d+)\)/')

        while from_date < self._max_date:

            print('type={0}, start={1}, end={2}'.format(self.doctypes, from_date, to_date))
            rsp = self.make_doctype_request(self.doctypes, from_date, to_date)
            while 'The number of results exceeded the maximum limit' in rsp.text:
                info = 'doc_type={0}, from_date={1}, to_date={2}'.format(self.doctypes, from_date,
                                                                         to_date)
                print("overflow with {0}".format(info))
                logging.getLogger().info("overflow with {0}".format(info), extra={'info': info})
                to_date = self._increment_days(to_date, -1)

                if to_date < from_date:
                    info = "from date: {0} < to_date {0}".format(from_date, to_date)
                    print(info)
                    logging.getLogger().warning(info, extra={'info': info})
                    from_date = self._increment_days(from_date, 1)
                    to_date = from_date + self._days_increment
                    break

                rsp = self.make_doctype_request(self.doctypes, from_date, to_date)
            rsp = requests.get(self.has_results,
                               #verify=os.environ.get('ca_cert', False),
                               cookies=self.session)
            if rsp.text != 'True':
                print("no results")
            else:
                databag = []
                data = {'page': '1', 'size': self.page_size}
                rsp = requests.post(self.grid_results,
                                    #verify=os.environ.get('ca_cert', False),
                                    cookies=self.session,
                                    data=urlencode(data, safe='&='),
                                    headers={'Content-Type': 'application/x-www-form-urlencoded',
                                             'X-Requested-With': 'XMLHttpRequest'})
                if rsp.status_code == 500:
                    data = {'page': '1', 'size': 500}
                    rsp = requests.post(self.grid_results,
                                        # verify=os.environ.get('ca_cert', False),
                                        cookies=self.session,
                                        data=urlencode(data, safe='&='),
                                        headers={'Content-Type': 'application/x-www-form-urlencoded',
                                                 'X-Requested-With': 'XMLHttpRequest'})
                    if rsp.status_code == 500:
                        logging.warning(F"unable to get data for {info}")
                        # go to next date range search
                        from_date = self._increment_days(to_date, 1)
                        to_date = from_date + self._days_increment
                        continue

                    _d = json.loads(rsp.text)
                    databag.extend(_d['data'])
                    if _d['total'] > 500:
                        for i in range(0, math.ceil(_d['total']/500)):
                            data = {'page': str(i+1), 'size': 500}
                            rsp = requests.post(self.grid_results,
                                                cookies=self.session,
                                                data=urlencode(data, safe='&='),
                                                headers={'Content-Type': 'application/x-www-form-urlencoded',
                                                         'X-Requested-With': 'XMLHttpRequest'})
                            __d = json.loads(rsp.text)
                            databag.extend(__d['data'])
                else:
                    json_data = json.loads(rsp.text)
                    databag.extend(json_data['data'])
                info = 'doc_type={0}, from_date={1}, to_date={2}'.format(self.doctypes, from_date,
                                                                         to_date)
                info = '{0} rec_count={1}'.format(str(len(databag)), info)
                m = "scraping page for {0}".format(info)
                print(m)
                logging.getLogger().info(m)

                for d in databag:
                    rdate = r_date_ex.match(d['RecordDate']).group(1)
                    try:
                        item = PBCPublicRecord(
                            party1=d['DirectName'].replace(',', ' '),
                            party2=d['IndirectName'].replace(',', ' '),
                            name=d['CompressedDirectName'],
                            cross_name=d['CompressedIndirectName'],
                            date=datetime.fromtimestamp(int(rdate[:10])).date().strftime('%m/%d/%Y'),
                            type_=self._doctype_maps[d['DocTypeDescription']],
                            book=d['BookPage'].split('/')[0] if len(d['BookPage'].split('/')) > 1 else '',
                            book_type=d['BookType'],
                            page=d['BookPage'].split('/')[1] if len(d['BookPage'].split('/')) > 1 else '',
                            pages='',
                            cfn=d['InstrumentNumber'],
                            legal=d.get('DocLegalDescription'),
                            info=info,
                            image_uri=self.image_url + str(d['TransactionItemId']),
                            consideration=d['Consideration']
                        )
                        yield item
                    except Exception as ex:
                        logging.getLogger().exception("error creating item: {0}".format(d))
                        continue
            # go to next date range search
            from_date = self._increment_days(to_date, 1)
            to_date = from_date + self._days_increment

            if from_date < self._max_date:
                if to_date > self._max_date:
                    info = 'doc_type={0}, from_date={1}, to_date={2}'.format(self.doctypes,
                                                                             from_date,
                                                                             to_date)
                    print("to_date: > maxdate: for {0} ; Maxdate is {1}".format(info, self._max_date))
                    to_date = self._max_date

            print("next date range search for:")

    def make_doctype_request(self, doctype, from_date, to_date):
        form_data = get_form_data(doctype, from_date, to_date)
        data = urlencode(form_data, safe='&=')
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        return requests.post(url=self.start_urls[0],
                             #verify=os.environ.get('ca_cert', False),
                             data=data,
                             headers=headers,
                             cookies=self.session)

    def parse(self, response):
        pass

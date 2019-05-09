import scrapy
from scrapy import signals
import requests
import json
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from collections import defaultdict
import os
import smtplib
from email.mime.text import MIMEText
import logging

from scrapers.mylogging import LogToMyDBHandler

#EMAILS = ['hfcdocsis@gmail.com',]
EMAILS = ['hfcdocsis@gmail.com', 'EZnVA@yahoo.com', 't.garcia@preceivables.com']


class MyBaseSpider(scrapy.Spider):

    name = None  # must implement this.
    loglevel = logging.ERROR  # override logging level in derived spider
    init_days_increment = 7

    def __init__(self, *args, **kwargs):
        super(MyBaseSpider, self).__init__(*args, **kwargs)
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
        self._keys = defaultdict(set)
        self.stats = kwargs['stats']

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        settings = crawler.settings
        kwargs['stats'] = crawler.stats
        kwargs['mysql_url'] = settings.get('MYSQL_URL')
        me = cls(*args, **kwargs)
        me._set_crawler(crawler)

        if os.environ.get('supress_email_notifications', None):
            return me
        crawler.signals.connect(me.spider_open, signal=signals.spider_opened)
        crawler.signals.connect(me.spider_close, signal=signals.spider_closed)
        crawler.signals.connect(me.setup_custom_logging, signal=signals.engine_started)
        return me

    def setup_custom_logging(self):
        # Where are doing some custom logging b/c we lose the default logging functionality from doing request nonasync
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        hndlr = LogToMyDBHandler(self.mysql_url, self.log_id)
        hndlr.setLevel(self.loglevel)
        root_logger.addHandler(hndlr)

    # todo: lookup email from user who sched. scrape
    def spider_close(self):
        url = self.settings['WEB_API_URL']
        rsp = requests.get(url + 'sites')
        try:
            assert rsp.status_code == 200, "unable to lookup site"
        except AssertionError:
            send_email(
                rcpts=EMAILS,
                subject="Debthound ETL Failure",
                msg=F"unable to lookup site info fot {url}")
            return

        sites = rsp.json()
        site = next(iter([s for s in sites if s['spider_name'] == self.name]))
        rsp = requests.post('{0}{1}'.format(url, 'runSiteETLs'), data=json.dumps(site),
                          headers={"Content-Type": "application/json"})
        send_email(rcpts=EMAILS, subject="Debthound ETL",
                   msg="Scrape run with {0} errors ETL ran {1}".format(
                       self.stats.get_value('log_count/ERROR', '0'),
                       "successfully" if rsp.status_code == 200 else "unsuccessful"))

    def spider_open(self):
        url = self.settings['WEB_API_URL']
        rsp = requests.get(url + 'sites')
        try:
            assert rsp.status_code == 200, "unable to lookup site"
        except AssertionError:
            send_email(rcpts=EMAILS, subject="Debthound ETL", msg=F"unable to lookup site info for {url}")
            return

        sites = rsp.json()
        site = next(iter([s for s in sites if s['spider_name'] == self.name]))
        send_email(rcpts=EMAILS,
                   subject="Debthound Scrape started",
                   msg="We just kicked off a scrape for {0}".format(site['base_url']))

    @staticmethod
    def _increment_days(begin_date, days):
        return begin_date + relativedelta(days=days)

    def check_key(self, key, value):
        if key in self._keys[value]:
            return True
        self._keys[value].add(key)
        return False


def send_email(rcpts, subject, msg):
    m = MIMEText(msg)
    m['Subject'] = subject
    m['From'] = 'debthound@li174-210.members.linode.com'
    m['To'] = ', '.join(rcpts)
    s = smtplib.SMTP('localhost', port=25)
    s.send_message(m)

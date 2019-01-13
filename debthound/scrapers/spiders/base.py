import scrapy
from scrapy import signals
import requests
import json
from dateutil.relativedelta import relativedelta
from collections import defaultdict
import os
import smtplib
from email.mime.text import MIMEText

#EMAILS = ['hfcdocsis@gmail.com',]
EMAILS = ['hfcdocsis@gmail.com', 'EZnVA@yahoo.com' 't.garcia@preceivables.com']


class MyBaseSpider(scrapy.Spider):

    name = None  # must implement this.

    def __init__(self, *args, **kwargs):
        super(MyBaseSpider, self).__init__(*args, **kwargs)
        self._keys = defaultdict(set)
        self.stats = kwargs['stats']

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        settings = crawler.settings
        sql = settings.get('MYSQL_URL')
        me = cls(stats=crawler.stats, mysql_url=sql, **kwargs)
        me._set_crawler(crawler)

        if os.environ.get('supress_email_notifications', None):
            return me
        crawler.signals.connect(me.spider_open, signal=signals.spider_opened)
        crawler.signals.connect(me.spider_close, signal=signals.spider_closed)
        return me

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

from datetime import datetime
from logging import getLogger
from scrapy.extensions.logstats import LogStats
from data_api.models import SessionContext, SiteScrapeLog, Site, SiteScrapeLogDetails

from scrapy.exceptions import NotConfigured
from scrapy import signals
from scrapy import log
from scrapy import logformatter


class LogToDatabase(LogStats):
    def __init__(self, *args, **kwargs):
        super(LogToDatabase, self).__init__(*args)
        mysql_url = kwargs['mysql_url']
        self.session_ctx = SessionContext(mysql_url, logger=getLogger())
        self.session_id = None

    @classmethod
    def from_crawler(cls, crawler):
        interval = crawler.settings.getfloat('LOGSTATS_INTERVAL')
        mysql_url = crawler.settings['MYSQL_URL']
        if not interval:
            raise NotConfigured
        o = cls(crawler.stats, interval, mysql_url=mysql_url)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(o.start_log, signal=signals.spider_opened)
        crawler.signals.connect(o.close_log, signal=signals.spider_closed)
        return o

    def log(self, spider):
        if self.session_id:
            with self.session_ctx as session:
                items = self.stats.get_value('item_scraped_count', 0)
                pages = self.stats.get_value('response_received_count', 0)
                irate = (items - self.itemsprev) * self.multiplier
                prate = (pages - self.pagesprev) * self.multiplier
                self.pagesprev, self.itemsprev = pages, items
                log_args = {'pages': pages, 'pagerate': prate, 'items': items, 'itemrate': irate}
                msg = ("Crawled {pages} pages (at {pagerate} pages/min), "
                       "scraped {items} items (at {itemrate} items/min)".format(**log_args))
                info = spider.crawler.stats.get_value('{0}__request_info__'.format(spider.id))
                detail = SiteScrapeLogDetails(
                    site_scrape_log_id=self.session_id,
                    message=msg, info=info
                )
                session.add(detail)
                session.commit()

    def start_log(self, spider):
        with self.session_ctx as s:
            site = s.query(Site).filter_by(base_url=spider.id).one()
            log = SiteScrapeLog(
                start_datetime=datetime.utcnow(),
                params='start_date: {0}, end_date: {1}'.format(spider._from_date, spider._max_date),
                site_id=site.id, site=site
            )
            s.add(log)
            s.commit()
            self.session_id = log.id
            spider.log_id = log.id

    def close_log(self, spider):
        if self.session_id:
            with self.session_ctx as s:
                log = s.query(SiteScrapeLog).filter_by(id=self.session_id).one()
                log.end_datetime = datetime.utcnow()
                log.error = self.stats.get_value('log_count/ERROR', '0')
                site = s.query(Site).filter_by(base_url=spider.id).one()
                if site.last_scrape_datetime and site.last_scrape_datetime.date() < spider._max_date:
                    site.last_scrape_datetime = spider._max_date
                s.commit()

    def log_error(self, failure, response, spider):
        if self.session_id:
            with self.session_ctx as s:
                detail = SiteScrapeLogDetails(
                    site_scrape_log_id=self.session_id,
                    message=failure.value, info=response
                )
                s.add(detail)
                s.commit()


class MyLogFormatter(logformatter.LogFormatter):
    def dropped(self, item, exception, response, spider):
        original = super(MyLogFormatter, self).dropped(item, exception, response, spider)
        original['level'] = log.DEBUG
        return original
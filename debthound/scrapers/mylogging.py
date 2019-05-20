import logging
from data_api.models import SessionContext, SiteScrapeLog, Site, SiteScrapeLogDetails


class LogToMyDBHandler(logging.Handler):
    def __init__(self, sql_conn_str, log_id):
        super(LogToMyDBHandler, self).__init__(logging.INFO)
        self.session_ctx = SessionContext(sql_conn_str)
        self.log_id = log_id

    def emit(self, record):
        with self.session_ctx as session:
            msg = "level: %(levelno)s msg: %(message)s" % record.__dict__
            info = record.__dict__.get('info', '')
            if record.exc_info:
                info = str(record.exc_text)
            detail = SiteScrapeLogDetails(
                site_scrape_log_id=self.log_id,
                message=msg[:1000], info='%(info)s' % {'info': info[:1000]}
            )
            session.add(detail)
            session.commit()

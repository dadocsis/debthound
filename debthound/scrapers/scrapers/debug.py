import os
import logging

import appdirs
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


path = appdirs.user_data_dir('debthound')
if not os.path.exists(path):
    os.makedirs(path)

logger = logging.getLogger('')
logger.setLevel(logging.INFO)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(console)

file = logging.FileHandler(
    filename=os.path.join(path, 'pbc.log'),
    mode='w'
)
file.setLevel(logging.INFO)

logger.addHandler(file)

settings = get_project_settings()
settings.set('MYSQL_URL', 'mysql+pymysql://root:alishappy@localhost/debthound')
settings.set('LOG_LEVEL', 'INFO')
process = CrawlerProcess(settings)
process.crawl('pbc',
              start_date='12/10/2009',
              end_date='12/17/2009',
              doctypes='JUD C')
process.start()
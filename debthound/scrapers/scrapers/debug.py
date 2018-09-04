import os
import logging

import appdirs
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


path = appdirs.user_data_dir('debthound')
if not os.path.exists(path):
    os.makedirs(path)

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

logger.addHandler(console)

file = logging.FileHandler(
    filename=os.path.join(path, 'pbc.log'),
    mode='w'
)
file.setLevel(logging.ERROR)

logger.addHandler(file)

settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl('pbc')
process.start()
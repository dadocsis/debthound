import os
import logging
import argparse

import appdirs
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

parser = argparse.ArgumentParser()
parser.add_argument("-s", type=str, dest='spider',
                    help="spider name",
                    required=True)
parser.add_argument("-start", type=str, dest='start_date',
                    help="start date",
                    required=True)
parser.add_argument("-end", type=str, dest='end_date',
                    help="end date",
                    required=True)

args = parser.parse_args()
spider = args.spider
start_date = args.start_date
end_date = args.end_date
path = appdirs.user_data_dir('debthound')
if not os.path.exists(path):
    os.makedirs(path)

logger = logging.getLogger('')
logger.setLevel(logging.INFO)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(console)

file = logging.FileHandler(
    filename=os.path.join(path, spider + '.log'),
    mode='w'
)
file.setLevel(logging.INFO)

logger.addHandler(file)

settings = get_project_settings()
settings.set('LOG_LEVEL', 'INFO')
process = CrawlerProcess(settings)
process.crawl(spider, start_date=start_date, end_date=end_date)
process.start()

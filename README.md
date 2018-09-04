
set http_proxy=http://localhost:17560
scrapy crawl pbc -s FEED_URI="file:///c:\users\az0001\Documents\scrape\pbc.csv" -s FEED_FORMAT=csv -a start_date=09/03/2008 -a end_date=09/03/2018 -s LOG_FILE="c:\\users\\az0001\\Documents\\scrape\\log.txt" -s LOG_LEVEL=INFO

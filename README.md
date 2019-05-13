## DB setup:
- create debthound db
- migrate:
    - ```alembic -x url=mysql+pymysql://user:****@localhost/debthound revision --autogenerate```
    - ```alembic -x url=mysql+pymysql://user:****@localhost/debthound upgrade head```


set http_proxy=http://localhost:17560

##to file
```scrapy crawl pbc -s FEED_URI="file:///c:\users\az0001\Documents\scrape\pbc.csv" -s FEED_FORMAT=csv -a start_date=09/03/2008 -a end_date=09/03/2018 -s LOG_FILE="c:\\users\\az0001\\Documents\\scrape\\log.txt" -s LOG_LEVEL=INFO```
##to database
```scrapy crawl pbc -s MYSQL_URL=mysql+pymysql://user:pw@localhost/debthound -a start_date=01/03/2011 -a end_date=01/04/2011 -s LOG_FILE="c:\\users\\Al\\Documents\\scrape\\log.txt" -s LOG_LEVEL=INFO```

##flask setup
- copy secrets file
- run web_api init

##basic deploy instructions
- git pull
- (from debthound library folder)sudo rsync -vP debthound/ /opt/debthound/debthound
- sudo su
- cd /opt/debthound/debthound
- . /opt/debthound/py_venv/bin/activate
- python setup.py install
- systemctl restart httpd
[web]
- cd src/debthound/web/
- npm install
- npm run-script build
- rsync -avP /home/dadocsis/src/debthound/web/build/  /var/www/debthound/



##deploy spiders to scrapyd
- add site and sitedocs
- pip install scrapyd-client
- if lower env must set ENV=local (if local) need to do this before running scrapy d
- cd into root dir (where scrapyd.cfg lives)
- run scrapyd 
- scrapyd-deploy default -p debthound

## Prod (Dont for get to set Prod settings)

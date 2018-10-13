# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

import logging
import json

import scrapy
from scrapy.exceptions import DropItem
from scrapy.utils.serialize import ScrapyJSONEncoder
import requests

from scrapers.items import PBCPublicRecord
from data_api import models


class ScrapersPipeline(object):
    url = 'http://127.0.0.1:5000/api/v1/'

    def __init__(self, mysql_url, id, stats):
        self.session_ctx = models.SessionContext(mysql_url, logger=logging.getLogger())
        self.id = id  # the base_url
        self.stats = stats
        self.site_doctypes = {}
        self.site_id = None
        self._keys = set()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings['MYSQL_URL'], crawler.spidercls.id, crawler.stats)

    def process_item(self, item: PBCPublicRecord, spider):
        with self.session_ctx as session:
            # todo put urls in settings
            url = self.url
            if item['type_'] not in self.site_doctypes:
                rsp = requests.get(url + 'sites')
                assert rsp.status_code == 200, "unable to lookup site"
                sites = rsp.json()
                site = next(iter([s for s in sites if s['base_url'] == self.id]))
                assert site, "site not found"
                self.site_id = site['id']

                rsp = requests.get(url + 'site_doc_type/{0}'.format(site['id']))
                assert rsp.status_code == 200, "unable to lookup site_doc_types"
                dts = rsp.json()
                self.site_doctypes = {d['name']: d for d in dts}

            doctype = self.site_doctypes[item['type_']]
            # check memory
            if self.check_key(item['cfn']):
                raise DropItem("item already exists: cfn={0}, info={1}", item['cfn'], item['info'])
            # double check server
            rsp = requests.get(url + 'documents/cfn/{0}'.format(item['cfn']))
            if rsp.status_code == 200:
                raise DropItem("item already exists: cfn={0}, info={1}", item['cfn'], item['info'])

            document = dict(
                book=item['book'], book_type=item['book_type'],
                cfn=item['cfn'], consideration=float(item['consideration']),
                cross_name=item['cross_name'], date=datetime.strptime(item['date'], '%m/%d/%Y').date(),
                image_uri=item['image_uri'], legal=item['legal'],
                page=item['page'], party1=",".join(item['party1']),
                party2=",".join(item['party2']), doctype_id=doctype['id'],
                site_id=self.site_id, name=item['name'], info=item['info']
            )
            return self.make_save_request(document, spider)

    def make_save_request(self, data, spider):
        _json = json.dumps(data, cls=ScrapyJSONEncoder)
        request = scrapy.Request(self.url + 'documents',
                                 method='POST',
                                 body=_json,
                                 headers={'Content-Type': 'application/json'})
        dfd = spider.crawler.engine.download(request, spider)
        dfd.addBoth(self.saved, _json)
        return dfd

    def saved(self, response, document):
        if response.status != 201:
            raise DropItem("Unable to save {0}".format(document))
        return document

    def check_key(self, key):
        if key in self._keys:
            return True
        self._keys.add(key)
        return False

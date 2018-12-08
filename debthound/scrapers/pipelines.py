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
import os
from data_api import models

doc_type_code_map = {
    'SAT':  'SAT',
    'JUD C': 'JUD C',
    'D': 'D',
    '168': 'JUD C',
    '138': 'D'
}


class ScrapersPipeline(object):

    def __init__(self, id, stats, web_api_url):
        self.id = id  # the base_url
        self.stats = stats
        self.site_doctypes = {}
        self.site_id = None
        self._keys = set()
        self.url = web_api_url

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.spidercls.id, crawler.stats, crawler.settings['WEB_API_URL'])

    def process_item(self, item: PBCPublicRecord, spider):
        url = self.url
        if doc_type_code_map[item['type_']] not in self.site_doctypes:
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

        doctype = self.site_doctypes[doc_type_code_map[item['type_']]]
        # check memory
        if self.check_key(item['cfn']):
            raise DropItem("item already exists: cfn={0}, info={1}", item['cfn'], item['info'])
        # double check server
        rsp = requests.get(url + 'documents/cfn/{0}'.format(item['cfn']))
        if rsp.status_code == 200:
            raise DropItem("item already exists: cfn={0}, info={1}", item['cfn'], item['info'])

        legal = item['legal'][:200] if item['legal'] else ''
        document = dict(
            book=item['book'], book_type=item['book_type'],
            cfn=item['cfn'], consideration=float(item['consideration']),
            cross_name=item['cross_name'], date=datetime.strptime(item['date'], '%m/%d/%Y').date(),
            image_uri=item['image_uri'], legal=legal,
            page=item['page'], party1=",".join(item['party1']),
            party2=",".join(item['party2']), doctype_id=doctype['id'],
            site_id=self.site_id, name=item['name'], info=item['info']
        )
        return self.make_save_request(document, spider)

    def make_save_request(self, data, spider):
        if os.environ.get('test_run', None):
            return data

        _json = json.dumps(data, cls=ScrapyJSONEncoder)
        request = scrapy.Request(self.url + 'documents',
                                 method='POST',
                                 body=_json,
                                 headers={'Content-Type': 'application/json'})
        dfd = spider.crawler.engine.download(request, spider)
        dfd.addBoth(self.saved, _json)
        return dfd

    def saved(self, response, document):
        if not hasattr(response, 'status') or response.status != 201:
            raise DropItem("Unable to save {0}".format(document))
        return document

    def check_key(self, key):
        if key in self._keys:
            return True
        self._keys.add(key)
        return False

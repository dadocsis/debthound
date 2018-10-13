# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PBCPublicRecord(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    cross_name = scrapy.Field()
    date = scrapy.Field()
    type_ = scrapy.Field()
    book = scrapy.Field()
    page = scrapy.Field()
    cfn = scrapy.Field()
    legal = scrapy.Field()
    book_type = scrapy.Field()
    party1 = scrapy.Field()
    party2 = scrapy.Field()
    pages = scrapy.Field()
    image_uri = scrapy.Field()
    consideration = scrapy.Field()
    info = scrapy.Field()

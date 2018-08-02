# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # 设计数据模型类似ORM
    spider_name = scrapy.Field()
    domain = scrapy.Field()
    url = scrapy.Field()
    url_hash = scrapy.Field()
    crawl_date = scrapy.Field()

    question = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    translated_content = scrapy.Field()
    html_content = scrapy.Field()
    project_link = scrapy.Field()
    info = scrapy.Field()

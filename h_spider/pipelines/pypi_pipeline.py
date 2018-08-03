# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
from h_spider.settings import *
from translate_api.translate_api import api


# save to mongodb
class MongoPipeline(object):
    def __init__(self):
        self.conn = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.conn.get_database(MONGO_DB)

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        collection = self.db.get_collection(spider.custom_settings.get('MONGO_COLLECTION'))
        item['translated_content'] = api(item['content'])
        collection.insert(dict(item))
        return item

    def close_spider(self, spider):
        self.conn.close()


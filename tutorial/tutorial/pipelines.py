# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import os
import re
import pymongo

class DataBasePipe:
    def __init__(self, mongo_config):
        self.mongo_config = mongo_config


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_config = dict(
                host=crawler.settings.get('MONGO_HOST'),
                port=crawler.settings.get('MONGO_PORT'),
                username=crawler.settings.get('MONGO_USER'),
                password=crawler.settings.get('MONGO_PASS'),
                db=crawler.settings.get('MONGO_DB'),
                collection=crawler.settings.get('MONGO_COLLECTION'),
            )
        )

    def open_spider(self, spider):
        # Connect to MongoDB database
        print("OPEN_SPIDER::DataBasePipe")
        self.client = pymongo.MongoClient(
            host=self.mongo_config['host'],
            port=self.mongo_config['port'],
            username=self.mongo_config['username'],
            password=self.mongo_config['password'],
        )
        # Lazyly create database and collection
        self.collection = self.client[
            self.mongo_config['db']][self.mongo_config['collection']
        ]


class MongoPipeline(DataBasePipe):

    def open_spider(self, spider):
        # Connect to MongoDB database
        print("OPEN_SPIDER::MongoPipeline")
        self.client = pymongo.MongoClient(
            host=self.mongo_config['host'],
            port=self.mongo_config['port'],
            username=self.mongo_config['username'],
            password=self.mongo_config['password'],
        )
        # Lazyly create database and collection
        self.collection = self.client[
            self.mongo_config['db']][self.mongo_config['collection']
        ]
        # Now sets `spider.min_required_id` to be the lower already seem `id`.
        # This works because HN  items `id` only increase monotonically
        # over time.
        if not self.collection.estimated_document_count():
            self.collection.create_index([('id', pymongo.ASCENDING)], unique=True)
            spider.min_required_id = 0
        else:
            cursor = self.collection.find().sort('id', pymongo.DESCENDING).limit(1)
            spider.min_required_id = list(cursor)[0]['id']
        if int(os.getenv('MIN_REQUIRED_ID', -1)) > 0:
            spider.min_required_id = int(os.getenv('MIN_REQUIRED_ID'))
            print("MIN_REQUIRED_ID manually specified.")
        else:
            print("MIN_REQUIRED_ID get from database.")
        print("MIN_REQUIRED_ID:", spider.min_required_id)


    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        if item['id'] > spider.min_required_id:
            try:
                self.collection.insert_one(item)
            except:
                print("[DEBUG-comment] DUPLICATED ID:", item['id'])
        else:
            pass
        return item


class AlertPipeline(DataBasePipe):
    """Pipeline for (conceptually) trigger an alarm when 'linux' word is present on item['text'].
    Actually the "alarm" consists on saving the comment **id** on a **linux_ids** collection.
    
    """
    

    def process_item(self, item, spider):
        if 'linux' in re.sub(r'\s+', '', item['text']):
            try:
                self.client[self.mongo_config['db']].linux_ids.insert_one({'id': item['id']})
            except:
                print("[DEBUG-comment-linux] DUPLICATED ID:", item['id'])
        return item

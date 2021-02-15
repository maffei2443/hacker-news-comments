# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter
from scrapy import exceptions

class MongoPipeline:


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
        # Now sets `spider.min_id` to be the lower already seem `id`.
        # This works because HN  items `id` only increase monotonically
        # over time.
        if not self.collection.estimated_document_count():
            self.collection.create_index([('id', pymongo.ASCENDING)], unique=True)
            spider.min_id = 0
        else:
            cursor = self.collection.find().sort('id', pymongo.DESCENDING).limit(1)
            spider.min_id = list(cursor)[0]['id']
        print("MIN_REQUIRED_ID:", spider.min_id)


    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item['id'] > spider.min_id:
            self.collection.insert_one(item)
        else:
            pass
        return item


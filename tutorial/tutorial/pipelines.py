# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter

class MongoPipeline:
    base_name = 'hackernews'
    collection_name = 'comments'

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
            )
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(**self.mongo_config)
        self.collection = self.client[self.base_name].db[self.collection_name]
        if not self.collection.estimated_document_count():
            self.collection.create_index([('id', pymongo.ASCENDING)], unique=True)


    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.collection.insert_one(item)
        print("INSERIU")
        return item


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient
from termcolor import colored
import warnings
import os
from dotenv import load_dotenv
from scrapy.exceptions import DropItem
load_dotenv()

class ValidationPipline:
    def process_item(self, item, spider):
        mandatory_attr = ["name", "url", "deadline", "is_definite", "loc", "is_loc_accurate"]
        arbitrary_attr = ["address", "wages", "type_of_job", "preferences", "es", "target", "working_hours", "work_period", "fetched_date", "jc", "jmc"]
        for attr in mandatory_attr:
            if attr not in item.keys():
                raise DropItem(colored(f"Missing {attr}! {item['url']}", 'red'))
        for attr in arbitrary_attr:
            if attr not in item.keys():
                warnings.warn(colored(f"Missing {attr}! {item['url']}", 'green'))

        return item

class MongoPipeline:
    def open_spider(self, spider):
        self.client = MongoClient(os.environ['DB_PATH'])
        self.db = self.client["scraping-book"]
        self.collection = self.db['item']
    
    def close_spider(self, spider):
        self.client.close()
        
    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item
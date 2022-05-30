import datetime
from http import client
from pydoc import cli
from backend.config import get_config
from pymongo import MongoClient

class OrganizeDB:
    def __init__(self):
        config=get_config()
        client = MongoClient(config.db_path)
        self.collection = client['scraping-book']['item']

    def drop_expired(self):
        now = datetime.datetime.now()
        for doc in self.collection.find({'deadline': {'$lt': now}}):
            self.collection.delete_one({"_id": doc["_id"]})
    
    def delete_dups(self): # https://qiita.com/sey323/items/700a47bf5f12e04fd4d0
        pipeline = [
            {"$group": {"_id": "$url", "dups": {"$addToSet": "$_id"}, "count": {"$sum": 1}}},
            {"$match": {"count": {"$gt": 1}}}
        ]    
        for doc in self.collection.aggregate(pipeline):
            doc['dups'].pop(-1) # leave latest one
            self.collection.delete_many({"_id": {"$in": doc['dups']}})
            
    def existing_urls(self) -> list:
        return [doc['url'] for doc in self.collection.find({}, {"url": True})]
            
def main():
    organizer = OrganizeDB()
    organizer.delete_dups()
    organizer.drop_expired()

if __name__ == "__main__":
    main()
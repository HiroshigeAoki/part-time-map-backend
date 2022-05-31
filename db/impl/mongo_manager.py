import logging
from typing import List, Dict

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from backend.db import DatabaseManager
from backend.db.models import Job, OID
from backend.query import Query


class MongoManager(DatabaseManager):
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect_to_database(self, path: str):
        logging.info("Connecting to MongoDB.")
        self.client = AsyncIOMotorClient(
            path,
            maxPoolSize=10,
            minPoolSize=10)
        self.db = self.client["scraping-book"]
        logging.info("Connected to MongoDB.")

    async def close_database_connection(self):
        logging.info("Closing connection with MongoDB.")
        self.client.close()
        logging.info("Closed connection with MongoDB.")

    async def search(self, query: Query) -> List[Job]:
        #TODO: 検索機能実装。
        criteria = (
            {
                "loc": {"$geoWithin":{"$centerSphere": [query.center_loc['coordinates'], query.radius / (6378.1 * 1000)]}},
            }
        )
        job_list = await self.db.item.find(criteria).to_list(1000)
        return job_list
            
    async def get_one_example(self) -> Job:
        job_q = await self.db.item.find_one()
        return Job(**job_q)
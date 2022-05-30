import logging
from typing import List

from fastapi import Query
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from backend.db import DatabaseManager
from backend.db.models import Job, OID


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
        jobs_list = []
        item_q = self.db.item.find()
        async for post in item_q:
            jobs_list.append(Job(**post))
        return jobs_list

    async def get_one_example(self) -> Job:
        job_q = await self.db.item.find_one()
        return Job(**job_q)
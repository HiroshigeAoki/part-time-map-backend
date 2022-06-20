import logging
from typing import List, Dict
import pandas as pd

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
        criteria_list = []
        if query.preferences:
            criteria_list.extend([{"preferences":{"$in":[pref]}} for pref in query.preferences])
        elif query.jc:
            criteria_list.extend([{"jc":{"$in":[jc]}} for jc in query.jc])
        elif query.jmc:
            criteria_list.extend([{"jmc":{"$in":[jmc]}} for jmc in query.jmc])
        
        # TODO:範囲の広さは後でもっかい考える。
        if query.commute.time is None or query.commute.time == 5: # commuteが指定されていない時 or 5分圏内は、2km圏内のみ 
            criteria_list.append({"loc": {"$geoWithin":{"$centerSphere": [query.origins['coordinates'], 2 / (6378.1)]}}})
        elif query.commute.time == 10:
            criteria_list.append({"loc": {"$geoWithin":{"$centerSphere": [query.origins['coordinates'], 10 / (6378.1)]}}})
        elif query.commute.time == 20:
            criteria_list.append({"loc": {"$geoWithin":{"$centerSphere": [query.origins['coordinates'], 15 / (6378.1)]}}})
        elif query.commute.time == 30:
            criteria_list.append({"loc": {"$geoWithin":{"$centerSphere": [query.origins['coordinates'], 20 / (6378.1)]}}})

        criteria = {"$and": criteria_list}
        job_list = await self.db.item.find(criteria).to_list(1000)
        def get_coordinates(series):
            return series.get('coordinates')
        #job_df = pd.DataFrame(job_list)
        #job_df['coordinates'] = job_df['loc'].apply(get_coordinates)
        #job_df['commute_time'] = job_df.apply(calc_commute_time)
        #job_df.query('commute_time >= query.commute.time')
        #job_list = job_df.to_dict()
        return job_list

    async def get_one_example(self) -> Job:
        job_q = await self.db.item.find_one()
        return Job(**job_q)
import logging
from typing import List, Dict
import requests
import pandas as pd
import os
import json
import time

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import status, HTTPException

from api.db import DatabaseManager
from api.db.models import Job, OID
from api.query import Query

from dotenv import load_dotenv
load_dotenv()

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
        start = time.time()
        criteria_list = []
        if query.preferences:
            criteria_list.extend([{"preferences":{"$in":[pref]}} for pref in query.preferences])
        elif query.jc:
            criteria_list.extend([{"jc":{"$in":[jc]}} for jc in query.jc])
        elif query.jmc:
            criteria_list.extend([{"jmc":{"$in":[jmc]}} for jmc in query.jmc])
        
        if query.commute.time is None or query.commute.time == 5 or query.commute.travelMode=="walking": # commuteが指定されていない時 or 5分圏内は、2km圏内のみ 
            criteria_list.append({"loc": {"$geoWithin":{"$centerSphere": [query.origins['coordinates'], 2 / (6378.1)]}}})
        elif query.commute.time == 10:
            criteria_list.append({"loc": {"$geoWithin":{"$centerSphere": [query.origins['coordinates'], 10 / (6378.1)]}}})
        elif query.commute.time == 20:
            criteria_list.append({"loc": {"$geoWithin":{"$centerSphere": [query.origins['coordinates'], 15 / (6378.1)]}}})
        elif query.commute.time == 30:
            criteria_list.append({"loc": {"$geoWithin":{"$centerSphere": [query.origins['coordinates'], 20 / (6378.1)]}}})
        elapsed_time = time.time() - start
        print ("elapsed_time(criteria):{0}".format(elapsed_time) + "[sec]")

        criteria = {"$and": criteria_list}
        job_list = await self.db.item.find(criteria).to_list(1000)
        elapsed_time = time.time() - start
        print ("elapsed_time(first):{0}".format(elapsed_time) + "[sec]")

        def get_coordinates(series):
            return f"{series.get('coordinates')[1]},{series.get('coordinates')[0]}"

        job_df = pd.DataFrame(job_list)
        job_df["coord"] = job_df["loc"].apply(get_coordinates)
        durations = []
        for i in range(0, len(job_df), 25):
            if len(job_df) - i < 25:
                destinations="|".join(job_df["coord"][i:])
            else:
                destinations="|".join(job_df["coord"][i:i+25])
            url = "https://maps.googleapis.com/maps/api/distancematrix/json" \
                + f"?origins={query.origins['coordinates'][1]},{query.origins['coordinates'][0]}" \
                + f"&destinations={destinations}" \
                + f"&mode={query.commute.travelMode}" \
                + f"&key={os.environ['API_KEY']}"
            response = json.loads(requests.request("GET", url).text)
            if len(response['rows']) == 0:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Distance Matrix returns nothing.')
            durations.extend([el['duration']['value'] if el['status'] == "OK" else 9999999 for el in response['rows'][0]['elements']])
        job_df['commute_time'] = durations
        
        job_df = job_df.query(f'commute_time <= {query.commute.time * 60}')
        job_list = list(job_df.T.to_dict().values())
        elapsed_time = time.time() - start
        print ("elapsed_time(second):{0}".format(elapsed_time) + "[sec]")
        return job_list

    async def get_one_example(self) -> Job:
        job_q = await self.db.item.find_one()
        return Job(**job_q)
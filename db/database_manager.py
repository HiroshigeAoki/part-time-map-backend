# https://github.com/michaldev/fastapi-async-mongodb/blob/f8f42c73b5c3cfff6de0258618aa28189d2e0afe/app/db/database_manager.py
from abc import abstractmethod
from typing import List, Literal
from geojson import Point

from backend.db.models import Job, OID
from backend.query import Query


class DatabaseManager(object):
    @property
    def client(self):
        raise NotImplementedError

    @property
    def db(self):
        raise NotImplementedError

    @abstractmethod
    async def connect_to_database(self, path: str):
        pass

    @abstractmethod
    async def close_database_connection(self):
        pass

    @abstractmethod
    async def search(self, query: Query) -> List[Job]:
        pass

    @abstractmethod
    async def get_one_example(self) -> Job:
        pass
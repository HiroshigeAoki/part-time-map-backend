from api.db.database_manager import DatabaseManager
from api.db.impl.mongo_manager import MongoManager

db = MongoManager()


async def get_database() -> DatabaseManager:
    return db
from pydantic import BaseModel, Field, BaseConfig
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from typing import Optional
from geojson import Point
from typing import List


# https://github.com/tiangolo/fastapi/issues/1515 excluded from_mongo()
# https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/
class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(str(v))
        except InvalidId:
            raise ValueError("Not a valid ObjectId")


class Job(BaseModel):
    id: OID = Field(alias="_id")
    url: str = Field()
    name: str = Field()
    preferences: List[str] = Field()
    fetched_date: datetime = Field()
    job_title: str = Field()
    wages: str = Field()
    target: str = Field()
    loc: Optional[Point] = Field(None)
    working_hours: str = Field()
    deadline: datetime = Field()
    address: str = Field()
    statuses: Optional[List[str]] = Field(None)
    
    class Config(BaseConfig):
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
        }
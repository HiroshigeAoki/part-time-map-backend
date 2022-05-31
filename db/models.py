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
    preferences: Optional[List[str]] = Field(None)
    fetched_date: datetime = Field()
    job_title: Optional[str] = Field(None)
    wages: Optional[str] = Field(None)
    target: Optional[str] = Field(None)
    loc: Optional[Point] = Field(None)
    working_hours: Optional[str] = Field(None)
    deadline: datetime = Field()
    address: Optional[str] = Field(None)
    statuses: Optional[List[str]] = Field(None)
    
    class Config(BaseConfig):
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
        }
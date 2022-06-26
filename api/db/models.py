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
    name: str = Field()
    url: str = Field()
    deadline: datetime = Field()
    is_definite: bool = Field()
    loc: Optional[Point] = Field()
    is_loc_accurate: bool = Field() # the loc value may be inaccurate
    address: Optional[str] = Field(None)
    wages: Optional[str] = Field(None)
    type_of_job: Optional[str] = Field(None)
    preferences: Optional[List[str]] = Field(None)
    es: Optional[List[str]] = Field(None) # employment status
    target: Optional[str] = Field(None)
    working_hours: Optional[str] = Field(None)
    work_period: Optional[str] = Field(None)
    fetched_date: datetime = Field(None)
    jc: Optional[str] = Field(None)
    jmc: Optional[str] = Field(None)
    
    class Config(BaseConfig):
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
        }
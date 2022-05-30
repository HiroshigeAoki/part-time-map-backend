from pydantic import BaseModel, Field
from geojson import Point, coords
from typing import Literal, List


class Query(BaseModel):
    center_loc: Point = Field(description='geojson')
    radius: Literal['300m', '500m', '1km', '2km', '3km', '5km', '10km', '15km', '20km', '30km'] = Field('2km')
    transp: Literal['徒歩', '自転車', 'バス', '電車'] = Field(None)
    preferences: List[Literal['長期歓迎', '大学生', '主婦・主夫']] = Field(None, description='後でオプションを追加') #TODO: 後でオプションを定義する。
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "center_loc": { "type": 'Point', "coordinates": [ 137.70524, 34.72374 ] },
                    "radius": "2km",
                    "transp": '徒歩',
                    "preferences": ['大学生', '長期歓迎']
                },
                {
                    "center_loc": { "type": 'Point', "coordinates": [ 137.70524, 34.72374 ] },
                    "radius": "2km",
                    "transp": None,
                    "preferences": None
                }
            ]
        }
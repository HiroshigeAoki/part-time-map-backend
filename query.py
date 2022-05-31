from pydantic import BaseModel, Field, root_validator
from geojson import Point, coords
from typing import Literal, List

class Commute(BaseModel):
    transp: Literal['徒歩', '自転車', 'バス', '電車'] = Field(None)
    time: Literal['5分', '10分', '20分', '30分'] = Field(None, description='通勤時間。選択肢は仮。')
    
    @root_validator
    def is_both_filled(cls, v):
        if all(v.values()):
            raise ValueError('Both transp and time is required if either one is filled.')
        return


class Query(BaseModel):
    center_loc: Point = Field(description='geojson')
    radius: Literal['300m', '500m', '1km', '2km', '3km', '5km', '10km', '15km', '20km', '30km'] = Field('2km', description='radiusかcoummuteどちらか一つのみ。')
    commute: Commute = Field(None)
    preferences: List[Literal['長期歓迎', '大学生', '主婦・主夫']] = Field(None, description='後でオプションを追加') #TODO: 後でオプションを定義する。
    
    @root_validator
    def radius_commute(cls, v):
        if all(v.values()) or not any(v.values()):
            raise ValueError('Either radius or commute is required and not both.')
        
    class Config:
        schema_extra = {
            "examples": [
                {
                    "center_loc": { "type": 'Point', "coordinates": [ 137.70524, 34.72374 ] },
                    "radius": "2km",
                    "commute": {"transp": "徒歩", "time": "5分"},
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
    def str_to_int(self):
        self.radius = int(self.radius.replace('km', '000').replace('m', '00'))
        self.commute = int(self.commute.replace('分', ''))
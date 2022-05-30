from fastapi import APIRouter, Depends, FastAPI

from backend.db import DatabaseManager, get_database
from backend.query import Query

router = APIRouter()
app = FastAPI()

# for debug
@router.get("/")
def hellow_world():
    return {"Hello world"}

# for debug
@router.get('/example')
async def get_one_example(db: DatabaseManager = Depends(get_database)):
    job = await db.get_one_example()
    return job

@app.get('/result/')
async def search(query: Query, db: DatabaseManager = Depends(get_database)):
    jobs = await db.search()
    return jobs
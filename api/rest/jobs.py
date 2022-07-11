from typing import Dict, List
from fastapi import APIRouter, Depends, status, HTTPException

from api.db import DatabaseManager, get_database
from api.db.models import Job
from api.query import Query

router = APIRouter()

# for debug
@router.get('/example')
async def get_one_example(db: DatabaseManager = Depends(get_database)) -> Job:
    job = await db.get_one_example()
    return job

@router.post('/search')
async def search(query: Query, db: DatabaseManager = Depends(get_database)) -> List[Job]:
    query.setup()
    jobs = await db.search(query)
    if len(jobs) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Job with given conditions not found.')
    return [Job(**job) for job in jobs]

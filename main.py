from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.config import get_config
from backend.db import db
from backend.rest import jobs

app = FastAPI(title='part-time-map')

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

app.include_router(jobs.router, prefix='/api/jobs')

@app.on_event("startup")
async def startup():
    config = get_config()
    await db.connect_to_database(path=config.db_path)


@app.on_event("shutdown")
async def shutdown():
    await db.close_database_connection()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
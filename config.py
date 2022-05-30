from functools import lru_cache

from pydantic import BaseSettings


class Config(BaseSettings):
    app_name: str = "part-time-map"
    db_path: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_config():
    return Config()
from pydantic import BaseSettings, Field


class Config(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')


config = Config()

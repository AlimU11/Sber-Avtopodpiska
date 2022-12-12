from pydantic import BaseSettings, Field

# # TODO: remove
# import os
# os.environ['DATABASE_URL'] = 'postgresql://postgres:postgres@localhost:5432/db'


class Config(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')


config = Config()

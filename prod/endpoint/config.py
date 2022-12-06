from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')
    hostname: str = Field(..., env='HOSTNAME')


settings = Settings()

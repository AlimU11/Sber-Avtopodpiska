from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')
    models_table: str = Field(..., env='MODELS_TABLE')
    metrics_table: str = Field(..., env='METRICS_TABLE')


settings = Settings()

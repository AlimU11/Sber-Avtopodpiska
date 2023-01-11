from pydantic import BaseSettings, Field


class Config(BaseSettings):
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    host: str = Field(..., env='POSTGRES_HOST')
    port: str = Field(..., env='POSTGRES_PORT')
    db: str = Field(..., env='POSTGRES_DB')
    raw_hits_table: str = Field(..., env='RAW_HITS_TABLE')
    raw_sessions_table: str = Field(..., env='RAW_SESSIONS_TABLE')
    models_table: str = Field(..., env='MODELS_TABLE')
    metrics_table: str = Field(..., env='METRICS_TABLE')
    preds_table: str = Field(..., env='PREDS_TABLE')
    chunksize: int = Field(..., env='CHUNKSIZE')
    query_path: str = Field(..., env='QUERY_PATH')


config = Config()

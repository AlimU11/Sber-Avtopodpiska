from pydantic import BaseSettings, Field

# # TMP FOR LOCAL RUN # TODO: remove
# import os
# os.environ['POSTGRES_USER'] = 'postgres'
# os.environ['POSTGRES_PASSWORD'] = 'postgres'
# os.environ['POSTGRES_HOST'] = 'localhost'
# os.environ['POSTGRES_PORT'] = '5432'
# os.environ['POSTGRES_DB'] = 'db'
# os.environ['RAW_HITS_TABLE'] = 'sber_avtopodpiska.raw_hits'
# os.environ['RAW_SESSIONS_TABLE'] = 'sber_avtopodpiska.raw_sessions'
# os.environ['MODELS_TABLE'] = 'scores.models'
# os.environ['METRICS_TABLE'] = 'scores.metrics'
# os.environ['PREDS_TABLE'] = 'scores.train_pred'
# os.environ['CHUNKSIZE'] = '100000'
# os.environ['QUERY_PATH'] = 'query.sql'


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

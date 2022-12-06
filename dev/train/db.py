from config import settings
from sqlalchemy import create_engine

engine = create_engine(settings.db_url)


def write(pipeline, metrics):
    pass

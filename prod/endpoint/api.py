import sqlalchemy
from config import settings
from fastapi import FastAPI

app = FastAPI()

hostname = settings.hostname
engine = sqlalchemy.create_engine(settings.db_url)


@app.get('/')
async def root():
    return _status()


@app.get('/status')
async def status():
    return _status()


def _status():
    status = {
        'status': 'ok',
        'from': hostname,
    }
    return status

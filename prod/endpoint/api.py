from typing import Optional

import dill
import pandas as pd
import sqlalchemy
from Config import config
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

engine = sqlalchemy.create_engine(config.db_url)

model = engine.execute(
    'select model from scores.models order by dt desc limit 1',
).scalar()

model = dill.loads(model)


class Item(BaseModel):
    utm_source: Optional[bool]
    utm_medium: Optional[bool]
    utm_campaign: Optional[str]
    utm_adcontent: Optional[str]
    utm_keyword: Optional[str]
    device_category: Optional[str]
    device_os: Optional[str]
    device_brand: Optional[str]
    device_model: Optional[str]
    device_screen_resolution: Optional[str]
    device_browser: str
    geo_country: Optional[str]
    geo_city: Optional[str]


class Items(BaseModel):
    items: list[Item]


@app.get('/')
async def root():
    return _status()


@app.get('/status')
async def status():
    return _status()


@app.post('/predict')
async def predict(items: Items):
    return {
        i: int(pred)
        for i, pred in enumerate(
            model.predict(
                pd.DataFrame([i.dict() for i in items.items]),
            ),
        )
    }


def _status():
    return {
        'status': 'ok',
        'from': config.hostname,
    }

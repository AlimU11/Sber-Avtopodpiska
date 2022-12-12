import dill
import pandas as pd
import sqlalchemy
from Config import config
from fastapi import FastAPI

app = FastAPI()

engine = sqlalchemy.create_engine(config.db_url)

# TODO: remove
model = engine.execute(
    'select model from scores.models where model_id = 11;',
).scalar()
model = dill.loads(model)

df = pd.DataFrame(
    [
        [
            False,
            False,
            'isYoUwVPnRHJczHiHQbB',
            'JNHcPlZPxEMWDnRiyoBf',
            None,
            'mobile',
            None,
            'Nokia',
            None,
            '412x823',
            'Chrome',
            'Russia',
            'Stavropol',
        ],
    ],
    columns=[
        'utm_source',
        'utm_medium',
        'utm_campaign',
        'utm_adcontent',
        'utm_keyword',
        'device_category',
        'device_os',
        'device_brand',
        'device_model',
        'device_screen_resolution',
        'device_browser',
        'geo_country',
        'geo_city',
    ],
)


@app.get('/')
async def root():
    return _status()


@app.get('/status')
async def status():
    return _status()


@app.get('/predict')
async def predict():
    import time  # TODO: remove

    start = time.time()
    preds = {i: int(pred) for i, pred in enumerate(model.predict(df))}
    print('PRED TIME', time.time() - start)
    return preds


def _status():
    status = {
        'status': 'ok',
        'from': config.hostname,
    }
    return status

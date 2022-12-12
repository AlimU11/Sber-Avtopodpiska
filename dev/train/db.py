import numpy as np
import psycopg2
from Config import config
from psycopg2.extensions import AsIs, register_adapter
from sqlalchemy import create_engine


def adapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)


def adapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)


register_adapter(np.float64, adapt_numpy_float64)
register_adapter(np.int64, adapt_numpy_int64)
engine = create_engine(f'postgresql://{config.user}:{config.password}@{config.host}:{config.port}/{config.db}')


def write(pipeline, metrics, train):
    model_id = __insert_models(pipeline)
    __insert_metrics(model_id, metrics)
    __insert_train_pred(model_id, train)


def __insert_models(pipeline):
    c = engine.execute(
        'INSERT INTO %s (model) VALUES (%s) RETURNING model_id',
        AsIs(config.models_table),
        pipeline,
    )

    return c.scalar()


def __insert_metrics(model_id, metrics):
    engine.execute(
        """INSERT INTO %s (model_id, tn, fp, fn, tp, roc_auc, f1_beta, feature_importance, corr)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        AsIs(config.metrics_table),
        model_id,
        *metrics,
    )


def __insert_train_pred(model_id, train):
    conn = psycopg2.connect(
        user=config.user,
        password=config.password,
        host=config.host,
        port=config.port,
        database=config.db,
    )

    with conn.cursor() as cursor:
        psycopg2.extras.execute_values(
            cursor,
            f"""
            INSERT INTO {config.preds_table} (model_id, fact, pred_proba) VALUES %s;
            """,
            ((model_id, y, y_pred) for y, y_pred in zip(train[0].values, train[1].astype(float))),
            page_size=config.chunksize,
        )

        conn.commit()

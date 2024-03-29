# import smote_variants as sv
import json
import pickle

import dill
import pandas as pd
import sqlalchemy
from category_encoders.cat_boost import CatBoostEncoder
from Config import config
from feature_engine.encoding import OneHotEncoder, RareLabelEncoder
from feature_engine.imputation import MeanMedianImputer
from feature_engine.outliers import Winsorizer
from feature_engine.wrappers import SklearnTransformerWrapper
from ModelWrapper import ModelWrapper
from sklearn.model_selection import train_test_split
from sklearn.pipeline import FunctionTransformer, Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

models_dict = {
    'XGBoost': XGBClassifier,
}

cities = pd.read_csv('ru_cities.csv')  # NOTE: ../../data/ru_cities.csv for local

preprocess = Pipeline(
    steps=[
        (
            'rare_label_encoder',
            RareLabelEncoder(
                n_categories=3,
                variables=[
                    'utm_campaign',
                    'utm_adcontent',
                    'device_brand',
                    'device_browser',
                    'geo_country',
                ],
            ),
        ),
        (
            'binary_encoder',
            OneHotEncoder(
                variables=[
                    'geo_country',
                    'device_category',
                ],
                drop_last_binary=True,
            ),
        ),
        (
            'imputer',
            MeanMedianImputer(
                variables=[
                    'population',
                ],
            ),
        ),
        (
            'category_encoder',
            CatBoostEncoder(),
        ),
        (
            'outliers',
            Winsorizer(
                tail='both',
                variables=[
                    'device_screen_height',
                    'population',
                ],
            ),
        ),
        (
            'scaler',
            SklearnTransformerWrapper(
                StandardScaler(),
                variables=[
                    'device_screen_height',
                    'population',
                ],
            ),
        ),
    ],
)


def read_data(query, engine, chunksize):
    dfl = []

    for chunk in pd.read_sql(query, con=engine, chunksize=chunksize):
        dfl.append(chunk)

    return pd.concat(dfl, ignore_index=True)


def pandas_preprocess(df, cities):
    import numpy as np
    import pandas as pd

    return (
        df.assign(
            utm_campaign=lambda _df: _df.utm_campaign.fillna('not_specified'),
            utm_adcontent=lambda _df: _df.utm_adcontent.fillna(
                'not_specified',
            ),
            utm_keyword=lambda _df: _df.utm_keyword.fillna('none'),
            device_category=lambda _df: _df.device_category.apply(
                lambda x: 'mobile' if x == 'tablet' else x,
            ),
            device_os=lambda _df: _df.device_os.apply(
                lambda x: (
                    'Macintosh'
                    if x == 'iOS'
                    else 'Windows'
                    if x == 'Windows Phone'
                    else 'undefined'
                    if pd.isna(x) or x == '(not set)'
                    else 'Linux'
                ),
            ),
            device_brand=lambda _df: _df.device_brand.apply(
                lambda x: (
                    'undefined'
                    if pd.isna(
                        x,
                    )
                    or x == '(not set)'
                    else x
                ),
            ),
            device_screen_height=lambda _df: _df.device_screen_resolution.apply(
                lambda x: x.split('x')[1],
            ).astype(np.uint16),
            device_browser=lambda _df: _df.device_browser.apply(
                lambda x: ('Safari' if x == 'Safari (in-app)' else x),
            ),
            geo_city=lambda _df: _df.geo_city.apply(
                lambda x: 'undefined' if x == '(not set)' else x,
            ),
            os_keyword=lambda _df: _df.device_os + '_' + _df.utm_keyword,
        )
        .merge(cities, left_on='geo_city', right_on='name', how='left')
        .drop(
            [
                'name',
                'device_model',
                'device_screen_resolution',
                'device_os',
                'utm_keyword',
            ],
            axis=1,
        )
    )


def get_params(args, X_train, y_train):
    raise NotImplementedError('Function `get_params` is not implemented. Provide path to config instead.')


def train(args, logger):
    engine = sqlalchemy.create_engine(
        f'postgresql://{config.user}:{config.password}@{config.host}:{config.port}/{config.db}',
    )

    with open(config.query_path, 'r') as f:
        query = f.read()

    logger.info('Reading data...')

    df = read_data(
        query.format(
            config.raw_hits_table,
            config.raw_sessions_table,
        ),
        engine,
        config.chunksize,
    )

    X, y = df.drop('target_action', axis=1), df.target_action
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train)

    params = None
    if args.config:
        with open(args.config, 'r') as f:
            params_dict = json.load(f)
            args.resampler = params_dict['resampler']
            args.model = list(params_dict['model'].keys())[0]
            params = params_dict['model'][args.model]
    else:
        params = get_params(args, X_train, y_train)

    pipeline = Pipeline(
        steps=[
            (
                'pandas_preprocess',
                FunctionTransformer(
                    pandas_preprocess,
                    kw_args={'cities': cities},
                ),
            ),
            ('sklearn_preprocess', preprocess),
        ],
    )

    X_train.index = range(X_train.shape[0])
    y_train.index = range(y_train.shape[0])

    model = ModelWrapper(
        # getattr(sv, args.resampler)(n_jobs=16),
        None,
        models_dict[args.model](**params),
    )

    X_train_transformed = pipeline.fit_transform(X=X_train, y=y_train)
    X_val = pipeline.transform(X_val)

    pipeline.steps.append(('model', model))

    logger.info('Fitting model...')

    pipeline.fit(X=X_train, y=y_train, model__eval_set=[(X_train_transformed, y_train), (X_val, y_val)])

    logger.info('Predicting on test set and saving results...')

    pred_proba = pipeline.predict_proba(X_test)
    evals_result = pickle.dumps(pipeline[-1].evals_result_)

    feature_importance = pickle.dumps(
        pd.DataFrame.from_dict(
            {
                k: v
                for k, v in zip(
                    pipeline[-2].feature_names_in_,
                    pipeline[-1].feature_importances_,
                )
            },
            orient='index',
            columns=['importance'],
        ),
    )

    corr = pickle.dumps(pipeline[:-1].transform(X_test).corr())
    pipeline = dill.dumps(pipeline)

    return pipeline, feature_importance, corr, evals_result, y_test, pred_proba

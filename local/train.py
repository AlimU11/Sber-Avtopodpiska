# import smote_variants as sv
import json

import dill
import pandas as pd
from category_encoders.cat_boost import CatBoostEncoder
from feature_engine.encoding import OneHotEncoder, RareLabelEncoder
from feature_engine.imputation import MeanMedianImputer
from feature_engine.outliers import Winsorizer
from feature_engine.wrappers import SklearnTransformerWrapper
from ModelWrapper import ModelWrapper
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import FunctionTransformer, Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

models_dict = {
    'XGBoost': XGBClassifier,
}

cities = pd.read_csv('../data/ru_cities.csv')

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


def read_data():

    hits = pd.read_csv('../data/ga_hits.csv', low_memory=False)
    sessions = pd.read_csv('../data/ga_sessions.csv', low_memory=False)

    events_list = [
        'sub_car_claim_click',
        'sub_car_claim_submit_click',
        'sub_open_dialog_click',
        'sub_custom_question_submit_click',
        'sub_call_number_click',
        'sub_callback_submit_click',
        'sub_submit_success',
        'sub_car_request_submit_click',
    ]

    media_advertising = [
        'QxAxdyPLuQMEcrdZWdWb',
        'MvfHsxITijuriZxsqZqt',
        'ISrKoXQCxqqYvAZICvjs',
        'IZEXUFLARCUMynmHNBGo',
        'PlbkrSYoHuZBWfYjYnfw',
        'gVRrcxiDQubJiljoTbGm',
    ]

    organic_traffic = ['organic', 'referral', '(none)']

    return pd.merge(
        hits.assign(
            target_action=lambda _df: _df.event_action.apply(
                lambda x: 1 if x in events_list else 0,
            ),
        )
        .groupby('session_id', as_index=False)
        .agg({'target_action': 'max'})[['session_id', 'target_action']],
        sessions.assign(
            utm_source=lambda _df: _df.utm_source.apply(
                lambda x: True if x in media_advertising else False,
            ),
            utm_medium=lambda _df: _df.utm_medium.apply(
                lambda x: True if x in organic_traffic else False,
            ),
        )[
            [
                'session_id',
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
            ]
        ],
        how='inner',
        left_on='session_id',
        right_on='session_id',
    ).drop('session_id', axis=1)


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
    raise NotImplementedError(
        'Function `get_params` is not implemented. Provide path to config instead.',
    )


def train(logger):

    logger.info('Reading data...')

    df = read_data()

    X, y = df.drop('target_action', axis=1), df.target_action
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train)

    with open('model_config.json', 'r') as f:
        params_dict = json.load(f)
        params_dict['resampler']
        model = list(params_dict['model'].keys())[0]
        params = params_dict['model'][model]

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
        models_dict[model](**params),
    )

    X_train_transformed = pipeline.fit_transform(X=X_train, y=y_train)
    X_val = pipeline.transform(X_val)

    pipeline.steps.append(('model', model))

    logger.info('Fitting model...')

    pipeline.fit(
        X=X_train,
        y=y_train,
        model__eval_set=[
            (X_train_transformed, y_train),
            (X_val, y_val),
        ],
    )

    logger.info('Predicting on test...')

    pred_proba = pipeline.predict_proba(X_test)

    logger.info('ROC AUC: {}'.format(roc_auc_score(y_test, pred_proba[:, 1])))

    with open('model.pkl', 'wb') as f:
        dill.dump(pipeline, f)

FROM alimu/base-python:latest as base

ENV PATH="/opt/venv/bin:${PATH}"

RUN pip install --no-cache-dir --upgrade \
        category-encoders==2.5.1.post0 \
        feature-engine==1.5.2 \
        # smote-variants==0.7.1 \
        dill==0.3.6 \
        xgboost==1.5.2 \
        optuna==3.0.3

FROM python:3.9.15-slim

RUN apt-get update -y && \
    apt-get install -y \
        libpq5 && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir /usr/src/app

COPY --from=base /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:${PATH}"

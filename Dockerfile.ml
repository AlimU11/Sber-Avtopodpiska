FROM alimu/base-python:latest as base

ENV PATH="/opt/venv/bin:${PATH}"

RUN pip install --no-cache-dir --upgrade \
        category-encoders \
        feature-engine \
        dill \
        xgboost \
        lightgbm \
        catboost

FROM python:3.9.15-slim

RUN apt-get update -y && \
    apt-get install -y \
        libpq5 && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir /usr/src/app

COPY --from=base /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:${PATH}"

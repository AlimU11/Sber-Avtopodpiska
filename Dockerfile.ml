FROM python:3.9.15-slim as base

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:${PATH}"

RUN pip install --no-cache-dir --upgrade \
        pip \
        numpy \
        pandas \
        psycopg2 \
        sqlalchemy \
        scikit-learn \
        xgboost \
        lightgbm \
        catboost \
        optuna

FROM python:3.9.15-slim

COPY --from=base /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:${PATH}"

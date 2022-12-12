CREATE SCHEMA IF NOT EXISTS sber_avtopodpiska;
CREATE SCHEMA IF NOT EXISTS scores;
CREATE SCHEMA IF NOT EXISTS ml_ops;

CREATE TABLE IF NOT EXISTS sber_avtopodpiska.raw_sessions (
    id SERIAL,
    session_id VARCHAR,
    client_id VARCHAR,
    visit_date DATE,
    visit_time TIME,
    visit_number INTEGER,
    utm_source VARCHAR,
    utm_medium VARCHAR,
    utm_campaign VARCHAR,
    utm_adcontent VARCHAR,
    utm_keyword VARCHAR,
    device_category VARCHAR,
    device_os VARCHAR,
    device_brand VARCHAR,
    device_model VARCHAR,
    device_screen_resolution VARCHAR,
    device_browser VARCHAR,
    geo_country VARCHAR,
    geo_city VARCHAR,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS sber_avtopodpiska.raw_hits (
    id SERIAL,
    session_id VARCHAR,
    hit_date DATE,
    hit_time FLOAT,
    hit_number INTEGER,
    hit_type VARCHAR,
    hit_referer VARCHAR,
    hit_page_path VARCHAR,
    event_category VARCHAR,
    event_action VARCHAR,
    event_label VARCHAR,
    event_value FLOAT,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS sber_avtopodpiska.attendance_book (

);

CREATE TABLE IF NOT EXISTS scores.models (
    model_id SERIAL PRIMARY KEY,
    model BYTEA NOT NULL,
    dt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scores.metrics (
    model_id INTEGER UNIQUE,
    tn FLOAT,
    fp FLOAT,
    fn FLOAT,
    tp FLOAT,
    roc_auc FLOAT,
    f1_beta FLOAT,
    feature_importance BYTEA,
    corr BYTEA,
    PRIMARY KEY (model_id),
    CONSTRAINT fk_model_id
        FOREIGN KEY (model_id)
            REFERENCES scores.models (model_id)
);

CREATE TABLE IF NOT EXISTS scores.train_pred (
    pred_id SERIAL,
    model_id INTEGER,
    fact INTEGER,
    pred_proba FLOAT,
    PRIMARY KEY (pred_id, model_id),
    CONSTRAINT fk_model_id
        FOREIGN KEY (model_id)
            REFERENCES scores.models (model_id)
);

CREATE TABLE IF NOT EXISTS ml_ops.trg_endpnt_perf (
    pred_id SERIAL,
    model_id INTEGER,
    pred_proba FLOAT,
    dt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (pred_id, model_id),
    CONSTRAINT fk_model_id
        FOREIGN KEY (model_id)
            REFERENCES scores.models (model_id)
);

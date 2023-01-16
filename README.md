[![wakatime](https://wakatime.com/badge/user/ec8c97a0-e0e3-4763-a6b4-374bde6dcd04/project/aafb6a03-63ca-4a74-a569-ba002e6c1af1.svg?style=for-the-badge)](https://wakatime.com/badge/user/ec8c97a0-e0e3-4763-a6b4-374bde6dcd04/project/aafb6a03-63ca-4a74-a569-ba002e6c1af1)

# Sber Avtopodpiska

Binary classification of Sber Avtopodpiska website visitors' interactions for predefined target actions. This project contains a full pipeline of data preparation and model training, as well as model deployment as an API endpoint. In addition, deploy other services such as a database to store initial data and training results (initial data is not included in the repository, but it is part of db image), scalable API endpoint, the dashboard for visualizing training results and services for collecting and visualizing metrics for database and endpoint performance.

## File Structure

```tree
Sber-Avtopodpiska
├─ .env
├─ .gitignore
├─ .pre-commit-config.yaml
├─ assets
│  └─ services.svg
├─ data
│  ├─ grafana-storage
│  └─ ru_cities.csv
├─ db-init
│  ├─ 00-postgres-init.sh
│  ├─ 01-init.sql
│  └─ 02-init.sh
├─ dev
│  ├─ dashboard
│  │  ├─ app.py
│  │  ├─ AppData.py
│  │  ├─ assets
│  │  │  └─ style.css
│  │  ├─ callbacks.py
│  │  ├─ Config.py
│  │  ├─ IdHolder.py
│  │  ├─ layout.py
│  │  ├─ utils.py
│  │  └─ wsgi.py
│  └─ train
│     ├─ config.py
│     ├─ db.py
│     ├─ main.py
│     ├─ metrics.py
│     ├─ ModelWrapper.py
│     ├─ model_config.json
│     ├─ Objectives.py
│     ├─ query.sql
│     └─ train.py
├─ docker-compose.yaml
├─ Dockerfile.api
├─ Dockerfile.base-python
├─ Dockerfile.dashboard
├─ Dockerfile.db
├─ Dockerfile.ml
├─ local
│  ├─ api.py
│  ├─ main.py
│  ├─ ModelWrapper.py
│  ├─ model.pkl
│  ├─ model_config.json
│  └─ train.py
├─ notebooks
│  ├─ EDA.ipynb
│  ├─ Model Selection.ipynb
│  └─ Preprocessing.ipynb
├─ prod
│  └─ endpoint
│     ├─ api.py
│     ├─ Config.py
│     ├─ ModelWrapper.py
│     └─ train.py
├─ prometheus.yaml
├─ README.md
└─ wait-for-it.sh
```

## Run

Docker setup requires approximately 15 GB RAM to run all services simultaneously or 5.8 GM RAM to run db + dev-train (most memory consumptive pair, the value highly depends on training settings - model, model parameters and resampler)

Run the following command in the root directory of the project:

```bash
docker-compose up db dev-train
```

at least once to train the model and save it to the database. Additionally, you can include the following services in the command:

- traefik
- adminer
- grafana
- postgres-exporter
- prometheus

After that you can up the following services:

- dev-dashboard
- endpoint

### Run locally

Alternatively, go to the `local` directory and run the following command:

```bash
python main.py
```

to initiate the training process. Consider putting respective data (`ga_hits.csv`, `ga_sessions.csv`) under the `data` directory beforehand.

Using the following command:

```bash
python -m uvicorn api:app --proxy-headers --host 127.0.0.1 --port 80
```

you can run the API locally.

## API

API accepts the following requests
- `GET` 
  - `/`, `/status` - return endpoint status. If running in container, additionally return container name
  - `/score` - for local endpoint only. Return ROC AUC score for model.
- `POST`
  - `/predict` - return predictions for one or more items. Each item should contain `utm_*`, `device_*` and `geo_*` data. The accepted format is dict with `items` key, that contains array with `dict`. Each `dict` in array represents one item. Example:

```json
{   
  "items": [
      {
          "utm_source": false,
          "utm_medium": false,
          "utm_campaign": "isYoUwVPnRHJ",
          "utm_adcontent": "JNHcPlZPxEM",
          "utm_keyword": null,
          "device_category": "mobile",
          "device_os": null,
          "device_brand": "Nokia",
          "device_model": null,
          "device_screen_resolution": "412x823",
          "device_browser": "Chrome",
          "geo_country": "Russia",
          "geo_city": "Stavropol"
      }
  ]
}
```


## Services

![assets/services](assets/services.svg)

1. ML - service for training models, making predictions on test data and saving models and metrics to a database.
2. Dev Dashboard - service for visualizing train results. Available at [http://dev-dashboard.localhost:8050](http://dev-dashboard.localhost:8050).

![assets/dashboard](assets/dashboard.png)
<p align="center" style="font-style: italic">(Dashboard example)</p>

3. Endpoint - service for making predictions on new data. Available at [http://api.localhost:80](http://api.localhost:80).
4. Prometheus - service for collecting metrics from services. Available at [http://prometheus.localhost:9090](http://prometheus.localhost:9090).
5. Grafana - service for visualizing metrics from database and API. Available at [http://grafana.localhost:3000](http://grafana.localhost:3000).
6. DB - service for storing data. Available at [http://db.localhost:5432](http://db.localhost:5432).
7. Adminer - service for database management. Available at [http://adminer.localhost:8090](http://adminer.localhost:8090).
8. Postgres-exporter - service for collecting metrics from a database.
9. Traefik - service for routing requests to services and API load balancer. In addition, allows to collect the metrics from API. Available at [http://traefik.localhost:8080](http://traefik.localhost:8080).

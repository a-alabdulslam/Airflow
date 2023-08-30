# Airflow

## Local env setup

For first-time setup, run the initialization container:

```powershell
mkdir -p ./logs,./plugins
docker-compose up airflow-init
```

Spin up a local dev environment by running:

```powershell
docker-compose up
```

When the following command starts to be printed periodically:

```powershell
airflow-webserver_1  | 127.0.0.1 - - [23/May/2023:08:57:35 +0000] "GET /health HTTP/1.1" 200 141 "-" "curl/7.74.0"
airflow-webserver_1  | 127.0.0.1 - - [23/May/2023:08:57:46 +0000] "GET /health HTTP/1.1" 200 141 "-" "curl/7.74.0"
airflow-webserver_1  | 127.0.0.1 - - [23/May/2023:08:57:56 +0000] "GET /health HTTP/1.1" 200 141 "-" "curl/7.74.0"
airflow-webserver_1  | 127.0.0.1 - - [23/May/2023:08:58:06 +0000] "GET /health HTTP/1.1" 200 141 "-" "curl/7.74.0"
```

The local environment is ready to be used and can be accessed in http://localhost:8080/.

When done, the local env could be turned off by simply quitting the terminal command (`ctrl + c`), stopping the containers using Docker Desktop, or by running:

```powershell
docker-compose down
```
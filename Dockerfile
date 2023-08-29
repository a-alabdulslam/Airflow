FROM apache/airflow:2.6.3
RUN pip install apache-airflow-providers-http==4.1.0
COPY ./dags/ /opt/airflow/dags
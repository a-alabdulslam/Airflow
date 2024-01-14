from datetime import datetime
from airflow import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.models.param import Param


with DAG(
    "sql_templates",
    default_args={
        "depends_on_past": False,
    },
    tags=["example6"],
    start_date=datetime(2021, 1, 1),
    catchup=False,
    render_template_as_native_obj=True,
    schedule_interval=None,
    params={
        "name": Param(default=None),
    },
) as dag:
    insert_name = SqliteOperator(
        sqlite_conn_id="db",
        task_id="insert_name",
        sql="query.sql",
        params={"name": "{{ parmas['name']}} "},
    )

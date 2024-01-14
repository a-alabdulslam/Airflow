from datetime import datetime
from airflow.decorators import dag
from airflow.operators.trigger_dagrun import TriggerDagRunOperator


@dag(
    "weather_scheduler",
    default_args={
        "depends_on_past": False,
    },
    tags=["example5"],
    start_date=datetime(2021, 1, 1),
    catchup=False,
    render_template_as_native_obj=True,
    schedule_interval="*/5 * * * *",
)
def taskflow():
    TriggerDagRunOperator(
        task_id="weather_follower",
        trigger_dag_id="weather_follower",
    )


taskflow()

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

def cats_info():
    from airflow.providers.http.hooks.http import HttpHook
    params = {
        "max_weight": 10,
        "playfulness": 5,
        "family_friendly": 3,
    }
    headers={
        "X-Api-Key":"qFRHN4uyV8Xoqyq2/cukNA==nofXB3oZvASzJF1R"
    }
    hook = HttpHook(http_conn_id="ninja_api", method="GET")
    response = hook.run("/cats", headers=headers,data=params).json()
    print(response)

with DAG(
    "cats",
    default_args={
        "depends_on_past": False,
    },
    tags=["example1"],
    start_date=datetime(2021, 1, 1),
    catchup=False,
    render_template_as_native_obj=True,
    schedule_interval=None,
) as dag:
    
    cats_info_task = PythonOperator(
        task_id="cats_info",
        python_callable=cats_info,
    )

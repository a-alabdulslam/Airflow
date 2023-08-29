from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models.param import Param

def get_citys():
    return ["Riyadh","London","Paris"]

def get_weather(citys):
    from airflow.providers.http.hooks.http import HttpHook
    import json
    headers={
        "X-Api-Key":"qFRHN4uyV8Xoqyq2/cukNA==nofXB3oZvASzJF1R"
    }
    for city in citys:
        params = {
            "city":city
        }
        hook = HttpHook(http_conn_id="ninja_api", method="GET")
        response = hook.run("/weather", headers=headers,data=params).json()

        with open(f'dags/Example3/output/{city}_current_weather.json', 'w') as outfile:
            json.dump(response, outfile)

with DAG(
    "weather",
    default_args={
        "depends_on_past": False,
    },
    tags=["example3"],
    start_date=datetime(2021, 1, 1),
    catchup=False,
    render_template_as_native_obj=True,
    schedule_interval=None,

) as dag:
    
    get_citys_task = PythonOperator(
        task_id="get_citys",
        python_callable=get_citys,
    )

    get_weather_task = PythonOperator(
        task_id="get_weather",
        python_callable=get_weather,
        op_kwargs={
            "citys": "{{ task_instance.xcom_pull('get_citys') }}",        
        },
    )

get_citys_task >> get_weather_task
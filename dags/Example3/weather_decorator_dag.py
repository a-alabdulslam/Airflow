from datetime import datetime
from airflow.decorators import task, dag

@task(task_id="get_citys")
def get_citys():
    return ["Riyadh","London","Paris"]

@task(task_id="get_weather")
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

        with open(f'dags/Example3/output_decorator/{city}_current_weather.json', 'w') as outfile:
            json.dump(response, outfile)

@dag(
    "weather_decorator",
    default_args={
        "depends_on_past": False,
    },
    tags=["example3"],
    start_date=datetime(2021, 1, 1),
    catchup=False,
    render_template_as_native_obj=True,
    schedule_interval=None,
) 
def taskflow():
    get_weather(get_citys())

taskflow()
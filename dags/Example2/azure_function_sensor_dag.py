from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor


def call_AF():
    import json
    from urllib.parse import urlparse, parse_qs
    from airflow.providers.http.hooks.http import HttpHook

    hook = HttpHook(http_conn_id="AF_url", method="GET")
    response = hook.run().json()
    status_query_get_uri = response["statusQueryGetUri"]
    parsed_url = urlparse(status_query_get_uri)
    path = parsed_url.path
    query = parsed_url.query

    endpoint = path + "?" + query
    return endpoint


def check_response(response):
    import json

    json_response = json.loads(response.content.decode("utf-8"))

    if json_response["runtimeStatus"] == "Completed":
        return True
    return False


with DAG(
    "azure_function_sensor",
    default_args={
        "depends_on_past": False,
    },
    tags=["example2"],
    start_date=datetime(2021, 1, 1),
    catchup=False,
    render_template_as_native_obj=True,
    schedule_interval=None,
) as dag:
    call_AF_task = PythonOperator(
        task_id="call_AF",
        python_callable=call_AF,
    )

    wait_for_AF = HttpSensor(
        task_id="wait_for_AF",
        http_conn_id="AF_check",
        endpoint="{{ti.xcom_pull('call_AF')}}",
        response_check=check_response,
        mode="reschedule",
        poke_interval=20,
        timeout=60,
    )

call_AF_task >> wait_for_AF

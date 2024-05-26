from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from pprint import pprint

default_args = {
    'owner': 'admin',
    'retries': 0,
    'retry_delay': timedelta(minutes=2),
    "catch_up": False
}

def receive_api(**context):
    dag_run = context.get("dag_run")
    pprint(context)
    my_value = dag_run.conf.get("my_key") if dag_run else None
    print(my_value)
    return my_value

with DAG(
    dag_id='api_test',
    default_args=default_args,
    description='test the rest api of airflow',
    start_date=datetime(2024, 2, 22),
    schedule_interval='@daily'
) as dag:

    receive_test_task = PythonOperator(
        task_id='received_api',
        python_callable=receive_api
    )

    receive_test_task
from datetime import datetime, timedelta
import logging
import json

from scraper.main import execute
# from .database_api import generate_payload, send_to_api

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator

from curl_cffi import requests

logger = logging.getLogger()
def generate_payload(**context):
    task_instance = context['task_instance']
    value = task_instance.xcom_pull(task_ids='scrape_targets', key='scraped_data')
    

def send_to_api(**context):
    task_instance = context['task_instance']
    # value = task_instance.xcom_pull(task_ids='airbnb_scrape', key='scraped_data')
    # value = {
    #     "test_only": "okay"
    # }
    values = task_instance.xcom_pull(task_ids='scrape_targets', key='scraped_data')
    for value in values:
        url = 'http://host.docker.internal:8000/api/data/properties/'
        headers = {
            'Content-Type': "application/json"
        }
        response = requests.post(url, headers=headers, impersonate='chrome110', json=value)
        if response.status_code in [200, 201]:
            logger.info('Successfully sent data to server')
        else:
            logger.info(f'Failed to send status {response.status_code}: {response.text}')
            raise Exception(f"Failed response, Status code {response.status_code}")


default_args = {
    'owner': 'admin',
    'retries': 0,
    'retry_delay': timedelta(minutes=2),
    "catch_up": False
}

def start_scraping(**context):
    logging.basicConfig(level = logging.INFO)
    # get config from the api
    task_instance = context['task_instance']
    configs = task_instance.xcom_pull(task_ids='fetch_config', key='return_value')
    results = []
    for config in configs:
        results.append({
            "task_id": config.get('task_id'),
            "scraped_data": execute(config)
        })
    
    task_instance.xcom_push(key='scraped_data', value=results)

with DAG(
    dag_id='airbnb_list_scraper',
    default_args=default_args,
    description='Scrape air bnb',
    start_date=datetime(2024, 2, 22),
    schedule_interval='@daily'
) as dag:
    
    fetch_config_task = SimpleHttpOperator(
        task_id='fetch_config',
        http_conn_id='nova_api_connection',
        method='GET',
        endpoint='/api/config/task/',
        response_filter = lambda response: json.loads(response.text)
    )

    scraping_task = PythonOperator(
        task_id='scrape_targets',
        python_callable=start_scraping
    )

    load_database_task = PythonOperator(
        task_id='load_to_database',
        python_callable=send_to_api
    )

    # fetch_config_task >> scraping_task

    # load_database_task
    fetch_config_task >> scraping_task >> load_database_task
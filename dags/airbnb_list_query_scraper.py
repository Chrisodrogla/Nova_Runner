from datetime import datetime, timedelta
import logging

from scraper.main import execute

from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'admin',
    'retries': 0,
    'retry_delay': timedelta(minutes=2),
    "catch_up": False
}

def start_scraping(**context):
    dag_run = context.get("dag_run")
    query = dag_run.conf.get("query") if dag_run else None
    logging.basicConfig(level = logging.INFO)
    execute(query=query)

with DAG(
    dag_id='airbnb_list_query_scraper',
    default_args=default_args,
    description='Scrape air bnb',
    start_date=datetime(2024, 2, 22),
    schedule_interval='@daily'
) as dag:

    scraping_task = PythonOperator(
        task_id='airbnb_scrape',
        python_callable=start_scraping
    )

    scraping_task
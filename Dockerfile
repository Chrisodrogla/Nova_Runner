FROM apache/airflow:2.1.1-python3.8

COPY requirements.txt /tmp/requirements.txt

COPY config/airflow.cfg /opt/airflow/airflow.cfg
RUN pip install --user --upgrade pip
RUN pip install -r /tmp/requirements.txt
COPY scraper /app
# RUN sudo groupadd -r airflow
USER root
RUN chown -R airflow /app/scraper/output
RUN chmod -R 777 /app/scraper/output

WORKDIR /app
USER airflow
RUN pip install -e .



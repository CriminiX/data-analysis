FROM apache/airflow:2.5.1

COPY ./requirements.txt .

RUN pip install --no-cache --user -r requirements.txt

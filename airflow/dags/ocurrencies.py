from datetime import datetime
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import (
    LocalFilesystemToS3Operator,
)
from airflow.models.variable import Variable
from ssp_extract import extract_statistics, StatisticType

default_args = {"start_date": datetime(2001, 1, 1)}


def delete_file(name):
    os.remove(name)


with DAG(
    "ssp_ocurrencies",
    default_args=default_args,
    schedule="@yearly",
    catchup=True,
    max_active_runs=2,
) as dag:
    filename = "{{ ds }}"
    execution_date = "{{ ds }}"
    partition = "{{ macros.ds_format(ds, '%Y-%m-%d', 'year=%Y') }}"
    bucket = Variable.get("bucket_raw_default", "tcc_raw")
    begin = EmptyOperator(task_id="begin")

    for t in StatisticType:
        type_name = t.name.lower()
        type_filename = f"{filename}_{type_name}.csv"
        extract_task = PythonOperator(
            task_id=f"extract_{type_name}",
            python_callable=extract_statistics,
            op_kwargs={"reference_date": execution_date, "default_filename": type_filename, "stats_type": t},
        )

        load_task = LocalFilesystemToS3Operator(
            task_id=f"load_{type_name}",
            dest_key=f"s3://{bucket}/ocurrencies/{type_name}/{partition}/{type_filename}",
            filename=type_filename,
            replace=True,
        )

        cleanup = PythonOperator(
            task_id=f"cleanup_{type_name}", python_callable=delete_file, op_kwargs={"name": type_filename}
        )

        begin >> extract_task >> load_task >> cleanup

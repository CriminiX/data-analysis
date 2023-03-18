from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from ssp_extract import extract_file
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from datetime import datetime
from airflow.models import Variable
import os

default_args = {
    "start_date": datetime(2003, 1, 1), 
}

def delete_file(name):
    os.remove(name)

with DAG(
    "ssp_extraction_to_s3", schedule="@monthly", catchup=True, max_active_runs=2, default_args=default_args
) as dag:
    filename = "{{ ds }}.xlsx"
    execution_date = "{{ ds }}"
    partition = "{{ macros.ds_format(ds, '%Y-%m-%d', 'year=%Y/month=%m') }}"
    bucket = Variable.get("bucket_raw_default", "tcc_raw")

    extract_task = PythonOperator(
        task_id="extract", python_callable=extract_file, 
        op_kwargs={"reference_date": execution_date, "default_filename": filename}
    )

    load_task = LocalFilesystemToS3Operator(
        task_id="load", 
        filename=filename, 
        dest_key=f"s3://{bucket}/car_theft/{partition}/{filename}",
        replace=True
    )

    cleanup = PythonOperator(
        task_id="cleanup",
        python_callable=delete_file,
        op_kwargs={"name": filename}
    )

    extract_task >> load_task >> cleanup

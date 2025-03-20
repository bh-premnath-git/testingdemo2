
from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.amazon.aws.operators.emr import EmrCreateJobFlowOperator, EmrTerminateJobFlowOperator, EmrAddStepsOperator
from airflow.operators.email import EmailOperator
from airflow.operators.bash import BashOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.utils.dates import days_ago
import logging
import os
 
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1
}

def success_callback(context):
    task_instance = context['task_instance'] 
    # Your custom logic here 
    print(f"Task {task_instance.task_id} succeeded.")

def execute_callback(context):
    task_instance = context['task_instance'] 
    # Your custom logic here 
    print(f"Task {task_instance.task_id} started.")
 
with DAG(
    dag_id='climate_cycledays',
    default_args=default_args,
    schedule_interval=None
) as dag:
    sensor_httpsensor_c5284d2e4 = HttpSensor(
        task_id='Sensor-HttpSensor-c5284d2e4',
        http_conn_id='http_connection_1',
        endpoint='httpbin.org/',
        response_check=lambda response: response.status_code == 200,
        timeout=300,
        poke_interval=5,
        on_execute_callback=execute_callback,
        on_success_callback=success_callback
    )

    # Set task dependencies

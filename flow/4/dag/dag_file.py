
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
    dag_id='climate_ycle',
    default_args=default_args,
    schedule_interval=None
) as dag:
    sensor_httpsensor_f99a8a7a_0c2a_4b2a_b5b0_4b9a3b8a2c1a = HttpSensor(
        task_id='Sensor-HttpSensor-f99a8a7a-0c2a-4b2a-b5b0-4b9a3b8a2c1a',
        http_conn_id='http_connection_1',
        endpoint='httpbin.org',
        response_check=lambda response: response.status_code == 200,
        timeout=300,
        poke_interval=5,
        on_execute_callback=execute_callback,
        on_success_callback=success_callback
    )
    custom_bashoperator_a1b2c3d4_e5f6_7890_1234_567890abcdef = BashOperator(
        task_id='Custom-BashOperator-a1b2c3d4-e5f6-7890-1234-567890abcdef',
        bash_command='echo "hello"',
        on_execute_callback=execute_callback,
        on_success_callback=success_callback
    )

    # Set task dependencies
    sensor_httpsensor_f99a8a7a_0c2a_4b2a_b5b0_4b9a3b8a2c1a >> custom_bashoperator_a1b2c3d4_e5f6_7890_1234_567890abcdef

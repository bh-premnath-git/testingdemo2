
from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.amazon.aws.operators.emr import EmrCreateJobFlowOperator, EmrTerminateJobFlowOperator, EmrAddStepsOperator
from airflow.providers.amazon.aws.sensors.emr import EmrStepSensor
from airflow.operators.email import EmailOperator
from airflow.operators.bash import BashOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1
}

with DAG(
    'dynamic_dag',
    default_args=default_args,
    schedule_interval=None
) as dag:

    sensor_simplehttpoperator_042944a29 = SimpleHttpOperator(
        task_id='Sensor-SimpleHttpOperator-042944a29',
        http_conn_id='http_connection_1',
        endpoint='/api/v1/resource',
        method='GET')
    

    # Set task dependencies


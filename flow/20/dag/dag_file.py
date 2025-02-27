
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
    dag_id='testflow1',
    default_args=default_args,
    schedule_interval=None
) as dag:
    sensor_s3keysensor_9818484b2 = S3KeySensor(
        task_id='Sensor-S3KeySensor-9818484b2',
        bucket_name='bh-dag-poc-1',
        bucket_key='job-input/test-airflow.txt',
        aws_conn_id='aws_connection_1',
        on_execute_callback=execute_callback,
        on_success_callback=success_callback
    )
    aws_emrcreateclusteroperator_97384076d = EmrCreateJobFlowOperator(
        task_id='AWS-EMRCreateClusterOperator-97384076d',
        aws_conn_id='aws_connection_1',
        emr_conn_id=None,
        wait_for_completion=True,
        job_flow_overrides={
    "Name": "DynamicEMRCluster",
    "ReleaseLabel": "emr-6.10.0",
    "LogUri": "s3://default-logs-emr/",
    "Instances": {
        "InstanceGroups": [
            {
                "Name": "Master node",
                "Market": "ON_DEMAND",
                "InstanceRole": "MASTER",
                "InstanceType": "m5.xlarge",
                "InstanceCount": 1
            },
            {
                "Name": "Core nodes",
                "Market": "ON_DEMAND",
                "InstanceRole": "CORE",
                "InstanceType": "m5.xlarge",
                "InstanceCount": 2
            }
        ],
        "Ec2SubnetId": "subnet-073f565d0ed9a5383",
        "EmrManagedMasterSecurityGroup": "sg-0c35439d413849b00",
        "EmrManagedSlaveSecurityGroup": "sg-0c35439d413849b00",
        "KeepJobFlowAliveWhenNoSteps": True,
        "TerminationProtected": False
    },
    "Applications": [
        {
            "Name": "Spark"
        }
    ],
    "VisibleToAllUsers": True,
    "JobFlowRole": "EMR_EC2_DefaultRole",
    "ServiceRole": "EMR_DefaultRole",
    "Steps": [
        {
            "Name": "Cluster Setup",
            "ActionOnFailure": "CONTINUE",
            "HadoopJarStep": {
                "Jar": "command-runner.jar",
                "Args": [
                    "bash",
                    "-c",
                    "\n                            set -euxo pipefail;\n\n                            echo \"Test started\";\n     \n                            # Download necessary files from S3\n                            aws s3 cp s3://bh-dag-poc-1/scripts/pipeline.py /tmp/pipeline.py\n                            aws s3 cp s3://bh-dag-poc-1/dependencies/bh_transformation_utils_wheel-0.1.tar.gz /tmp/bh_transformation_utils_wheel-0.1.tar.gz\n     \n                            # Validate downloaded files\n                            [ -f /tmp/pipeline.py ] || (echo \"pipeline.py not found\" && exit 1)\n                            [ -f /tmp/bh_transformation_utils_wheel-0.1.tar.gz ] || (echo \"bh_transformation_utils_wheel-0.1.tar.gz not found\" && exit 1)\n     \n                            # Install dependencies\n                            python3 -m pip install /tmp/bh_transformation_utils_wheel-0.1.tar.gz\n                            "
                ]
            }
        }
    ]
},
        on_execute_callback=execute_callback,
        on_success_callback=success_callback
    )
    transfer_sftpoperator_e3894baf6 = SFTPOperator(
        task_id='Transfer-SFTPOperator-e3894baf6',
        ssh_conn_id='default_ssh_conn',
        local_filepath='/path/to/local/file',
        remote_filepath='/path/to/remote/file',
        operation='put',
        create_intermediate_dirs=True,
        on_execute_callback=execute_callback,
        on_success_callback=success_callback
    )
    alert_emailoperator_156a4f5c5 = EmailOperator(
        task_id='Alert-EmailOperator-156a4f5c5',
        to='["Premnath@bighammer.ai"]',
        subject='Test Email',
        html_content="test",
        on_execute_callback=execute_callback,
        on_success_callback=success_callback
    )

    # Set task dependencies
    sensor_s3keysensor_9818484b2 >> aws_emrcreateclusteroperator_97384076d
    aws_emrcreateclusteroperator_97384076d >> transfer_sftpoperator_e3894baf6
    transfer_sftpoperator_e3894baf6 >> alert_emailoperator_156a4f5c5

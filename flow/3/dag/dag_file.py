
from airflow import DAG
from airflow.utils.dates import days_ago
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

default_args = {
    'owner': 'bh',
    'start_date': days_ago(1),
    'retries': 1
}

def success_callback(context):
    task_instance = context['task_instance'] 
    print(f"Task {task_instance.task_id} succeeded.")

def execute_callback(context):
    task_instance = context['task_instance'] 
    print(f"Task {task_instance.task_id} started.")

with DAG(
    dag_id='development_daily',
    default_args=default_args,
    schedule_interval=None
) as dag:


                from airflow.operators.bash import BashOperator
                custom_bashoperator_ba9a41dc9 = BashOperator(
                    task_id='Custom-BashOperator-ba9a41dc9',
                    bash_command='echo "list"
    ',
                    on_execute_callback=execute_callback,
                    on_success_callback=success_callback
                )


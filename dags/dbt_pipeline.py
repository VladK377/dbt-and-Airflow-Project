from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from scripts.adp_work import snowflake_pipeline




# Define default_args for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}






# Create the DAG
with DAG(
    dag_id='dbt_run_with_python_op',
    default_args=default_args,
    description='Run dbt models using PythonOperator',
    schedule_interval='0 9 * * *',  # Manual trigger or change as needed
    start_date=datetime(2025, 1, 12),
    catchup=False,
) as dag:

    # Bash command to run dbt
    dbt_run_command = """dbt run --project-dir /home/adp-workspace-venv/project"""

    # Create a task to run dbt using BashOperator
    dbt_run_task = BashOperator(
        task_id='dbt_run_task',
        bash_command=dbt_run_command,
    )


    snowflake_task = PythonOperator(
        task_id = 'SF_Task',
        python_callable= snowflake_pipeline,
    )

    dbt_run_task >> snowflake_task

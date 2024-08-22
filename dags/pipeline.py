from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG, the start date, and how frequently it runs
dag = DAG(
    'docker_spark_tasks',
    default_args=default_args,
    description='Run Spark jobs in Docker via Kafka',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 8, 21),
    catchup=False,
)

# Task 1: Execute Python script for Kafka stream
t1 = BashOperator(
    task_id='kafka_stream',
    # bash_command='docker exec node-master /usr/bin/python /home/spark/src/kafka/kafka_stream.py',
    bash_command='docker exec node-master /usr/bin/python /home/spark/src/kafka/kakfa_stream.py',
    dag=dag,
)

# Task 2: Submit Spark job to stream data to PostgreSQL
t2 = BashOperator(
    task_id='stream_to_postgres',
    bash_command='docker exec node-master /home/spark/src/spark/submit.sh /home/spark/src/spark/stream_to_postgres.py',
    dag=dag,
)

# Task 3: Submit Spark job for PostgreSQL analysis
t3 = BashOperator(
    task_id='postgres_analysis',
    bash_command='docker exec node-master /home/spark/src/spark/submit.sh /home/spark/src/spark/postgres_analysis.py',
    dag=dag,
)

# Set task dependencies
t1 >> t2 >> t3


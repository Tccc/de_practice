from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime


DAG_ID = "db_init"

default_args = {
    "owner": 'chernitskaia',
    "start_date" : datetime(2024, 6, 12),
    "retries": 1
}

with DAG(dag_id=DAG_ID,
    description='Dag to create schemas and tables',
    schedule_interval="@once",
    default_args=default_args,
    is_paused_upon_creation=False,
    max_active_runs=1,
    catchup=False
) as dag:

    start = EmptyOperator(task_id='START', dag=dag)

    init_log_schema = PostgresOperator(
        task_id=f'{DAG_ID}.init_log_schema',
        postgres_conn_id='postgres-db',
        sql='sql/log_schema_creation.sql',
    )

    init_ds_schema = PostgresOperator(
        task_id=f'{DAG_ID}.init_ds_schema',
        postgres_conn_id='postgres-db',
        sql='sql/ds_schema_creation.sql',
    )

    trigger_dag_data_loading = TriggerDagRunOperator(
        task_id=f'{DAG_ID}.trigger_workflow',
        trigger_dag_id='upsert_data'
    )

    (
        start
        >> [init_ds_schema, init_log_schema]
        >> trigger_dag_data_loading
    )
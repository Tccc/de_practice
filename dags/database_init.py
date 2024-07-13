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

    start = EmptyOperator(task_id='START')

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

    init_dm_schema = PostgresOperator(
        task_id=f'{DAG_ID}.init_dm_schema',
        postgres_conn_id='postgres-db',
        sql='sql/dm_schema_creation.sql',
    )

    plug = EmptyOperator(
        task_id = "plug"
    )

    init_procedure_writelog = PostgresOperator(
        task_id=f'{DAG_ID}.init_procedure_writelog',
        postgres_conn_id='postgres-db',
        sql='sql/procedure_writelog.sql',
    )

    init_procedure_fill_account_turnover_f = PostgresOperator(
        task_id=f'{DAG_ID}.init_procedure_fill_account_turnover_f',
        postgres_conn_id='postgres-db',
        sql='sql/procedure_fill_account_turnover_f.sql',
    )

    init_procedure_fill_f101_round_f = PostgresOperator(
        task_id=f'{DAG_ID}.init_procedure_fill_f101_round_f',
        postgres_conn_id='postgres-db',
        sql='sql/procedure_fill_f101_round_f.sql',
    )

    trigger_dag_data_loading = TriggerDagRunOperator(
        task_id=f'{DAG_ID}.trigger_workflow',
        trigger_dag_id='upsert_data'
    )

    (
        start
        >> [init_ds_schema, init_dm_schema, init_log_schema]
        >> plug
        >> [init_procedure_writelog, init_procedure_fill_account_turnover_f, init_procedure_fill_f101_round_f]
        >> trigger_dag_data_loading
    )
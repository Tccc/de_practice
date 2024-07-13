from datetime import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

DAG_ID = "call_fill_f101_round_f"

def print_hello(logical_date):
    print(logical_date)
    
default_args = {
   'owner': 'airflow',
   'start_date': datetime(2018, 2, 1),
   'end_date': datetime(2018, 2, 2),
}

with DAG(DAG_ID,
          schedule_interval="@monthly",
          default_args = default_args,
          catchup=True) as dag:

    dummy_operator = EmptyOperator(
        task_id='end'
    )
    
    call_fill_f101_round_f = PostgresOperator(
        task_id=f'{DAG_ID}.call_procedure',
        postgres_conn_id='postgres-db',
        sql="call dm.fill_f101_round_f((to_date('{{logical_date}}', 'yyyy-MM-dd') - interval '1 day')::date)",
        autocommit = True
    )
    
    (
        call_fill_f101_round_f>>dummy_operator
    )
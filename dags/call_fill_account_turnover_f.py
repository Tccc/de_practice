from datetime import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

DAG_ID = "call_fill_account_turnover_f"

def print_hello(logical_date):
    print(logical_date)
    
default_args = {
   'owner': 'airflow',
   'start_date': datetime(2018, 1, 1),
   'end_date': datetime(2018, 1, 31),
}

with DAG(DAG_ID,
          schedule_interval="@daily",
          default_args = default_args,
          catchup=True) as dag:

    dummy_operator = EmptyOperator(
        task_id='end'
    )
    
    call_fill_account_turnover_f = PostgresOperator(
        task_id=f'{DAG_ID}.call_procedure',
        postgres_conn_id='postgres-db',
        sql="call ds.fill_account_turnover_f(to_date('{{logical_date}}', 'yyyy-MM-dd'))",
        autocommit = True
    )
    
    (
        call_fill_account_turnover_f>>dummy_operator
    )
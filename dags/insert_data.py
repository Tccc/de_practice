import sys
from pathlib import Path

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python_operator import PythonOperator

from datetime import datetime


DAG_ID = 'upsert_data'
self_path = str(Path(__file__).parent.absolute())
sys.path.append(self_path)

def read_json(filepath):
    import json
    f = open(filepath)
    data = json.load(f)
    f.close()
    return data


def read_file(filepath, options, rename_columns=None, int_columns_to_cast=None, date_formats=None, float_columns_to_cast=None):
    import pandas

    def cast_int_columns(df, columns):
        if columns is not None:
            for column in columns:
                df[column] = pandas.to_numeric(df[column])

        return df


    def cast_date_columns(df, date_formats):
        if date_formats is not None:
            for column in date_formats:
                df[column['column_name']] = pandas.to_datetime(df[column['column_name']], format=column["format"]) 

        return df


    def cast_float_columns(df, float_columns_to_cast):
        if float_columns_to_cast is not None:

            for column in float_columns_to_cast:
                df[column['column_name']] = pandas.to_numeric(df[column['column_name']], errors='coerce')

        return df
    
    df = pandas.read_csv(f'{self_path}/files/{filepath}', delimiter=';', encoding='cp866')

    df = df[rename_columns.keys()]
    df.rename(columns=rename_columns,inplace=True)
    
    df = cast_int_columns(df, int_columns_to_cast)
    df = cast_date_columns(df, date_formats)
    df = cast_float_columns(df, float_columns_to_cast)

    return df

def load_files_to_ds(table_name):

    postgres_hook = PostgresHook('postgres-db')
    engine = postgres_hook.get_sqlalchemy_engine()

    with engine.begin() as conn:
        files = read_json(f'{self_path}/configurations/config_data.json')

        file = files.get(table_name)

        if file:
            df = read_file(filepath=file['filename'],
                       options=file['options'],
                       rename_columns=file.get("rename_columns"),
                       int_columns_to_cast=file.get('int_columns_to_cast'),
                       float_columns_to_cast=file.get('float_columns_to_cast'),
                       date_formats=file.get('date_formats'))
        
            df.to_sql(file['table'] + '_temp', conn, schema='ds', if_exists='append', index=False)

            for row in conn.exec_driver_sql(
                '''SELECT  STRING_AGG(a.attname, ',')
                    FROM pg_index i JOIN   pg_attribute a 
                                ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
        		    WHERE   i.indrelid = 'ds.''' + file['table'] + ''''::regclass AND i.indisprimary'''):
                primary_keys = row[0]
            
            update_column = ", ".join([f'"{col}" = EXCLUDED."{col}"' for col in df.columns])

            conn.exec_driver_sql(
                f'INSERT INTO ds.{file['table']} select * from ds.{file['table']}_temp ON CONFLICT ({primary_keys}) DO UPDATE SET {update_column}'
            )
            conn.exec_driver_sql(
                f'DROP TABLE ds.{file['table']}_temp'
            )
           
           ##LOGS
            conn.exec_driver_sql(
                f"""
                INSERT INTO logs.task_loading_logs (dag_id, task_id, source, destination, action_date, step, status) VALUES
                ('{DAG_ID}', '{table_name}', '{self_path}/files/{file['filename']}', '{file['table']}', NOW(), 'SAVE DATA', 'OK')
                """
            )
        else:
            ##LOGS
            conn.exec_driver_sql(
                f"""
                INSERT INTO logs.task_loading_logs (dag_id, task_id, source, destination, action_date, step, status) VALUES
                ('{DAG_ID}', '{table_name}', '{self_path}/files/{file['filename']}', '{file['table']}', NOW(), 'CONFIG FILE NOT FOUND', 'ERROR')
                """
            )
  

default_args = {
    "owner": 'chernitskaia',
    "start_date" : datetime(2024, 6, 12),
    "retries": 1
}

with DAG (
    dag_id=DAG_ID,
    default_args=default_args,
    description="Загрузка данных в ds",
    catchup=False,
    schedule="@once"
) as dag:
    
    start = DummyOperator(
        task_id="start"
    )

    ft_balance_f = PythonOperator(
        task_id=f'{DAG_ID}.ft_balance_f',
        python_callable=load_files_to_ds,
        op_kwargs={"table_name":"ft_balance_f"}
    )

    ft_posting_f = PythonOperator(
        task_id=f'{DAG_ID}.ft_posting_f',
        python_callable=load_files_to_ds,
        op_kwargs={"table_name":"ft_posting_f"}
    )

    md_account_d = PythonOperator(
        task_id=f'{DAG_ID}.md_account_d',
        python_callable=load_files_to_ds,
        op_kwargs={"table_name":"md_account_d"}
    )

    md_currency_d = PythonOperator(
        task_id=f'{DAG_ID}.md_currency_d',
        python_callable=load_files_to_ds,
        op_kwargs={"table_name":"md_currency_d"}
    )

    plug = DummyOperator(
        task_id = "plug"
    )

    md_exchange_rate_d = PythonOperator(
        task_id=f'{DAG_ID}.md_exchange_rate_d',
        python_callable=load_files_to_ds,
        op_kwargs={"table_name":"md_exchange_rate_d"}
    )

    md_ledger_account_s = PythonOperator(
        task_id=f'{DAG_ID}.md_ledger_account_s',
        python_callable=load_files_to_ds,
        op_kwargs={"table_name":"md_ledger_account_s"}
    )

    end = DummyOperator(
        task_id = "end"
    )

    (
        start
        >>[ft_balance_f, ft_posting_f, md_account_d]
        >>plug
        >>[md_currency_d, md_exchange_rate_d, md_ledger_account_s]
        >> end
    )
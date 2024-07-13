CREATE SCHEMA IF NOT EXISTS logs;

CREATE TABLE IF NOT EXISTS logs.task_loading_logs (
    dag_id VARCHAR(50) NOT NULL,
    task_id VARCHAR(100),
    source VARCHAR(100),
    destination VARCHAR(30),
    action_date TIMESTAMP NOT NULL,
    step VARCHAR(50),
    status VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dm.lg_messages (
    record_id serial,
	date_time timestamp,
	pid int,
	"message" text,
	message_type text,
	usename text, 
	datname text, 
	client_addr text, 
	application_name text,
	backend_start timestamp
);

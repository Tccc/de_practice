CREATE SCHEMA IF NOT EXISTS DS;

DROP TABLE IF EXISTS DS.FT_BALANCE_F;
CREATE TABLE DS.FT_BALANCE_F (
    on_date DATE not null,
    account_rk integer not null,
    currency_rk integer not null,
    balance_out real,
    PRIMARY KEY (on_date, account_rk)
);

DROP TABLE IF EXISTS DS.FT_POSTING_F;
CREATE TABLE DS.FT_POSTING_F (
    id integer,
    oper_date DATE not null,
    credit_account_rk integer not null,
    debet_account_rk integer not null,
    credit_amount real,
    debet_amount real,
    PRIMARY KEY (id, oper_date, credit_account_rk, debet_account_rk)
);

DROP TABLE IF EXISTS DS.MD_ACCOUNT_D;
CREATE TABLE DS.MD_ACCOUNT_D (
    data_actual_date DATE not null,
    data_actual_end_date DATE not null,
    account_rk integer not null,
    account_number VARCHAR(20) not null,
    char_type VARCHAR(1) not null,
    currency_rk integer not null,
    currency_code VARCHAR(3) not null,
    PRIMARY KEY (data_actual_date, account_rk)
);

DROP TABLE IF EXISTS DS.MD_CURRENCY_D;
CREATE TABLE DS.MD_CURRENCY_D (
    currency_rk integer not null,
    data_actual_date DATE not null,
    data_actual_end_date date,
    currency_code VARCHAR(3),
    code_iso_char VARCHAR(3),
    PRIMARY KEY (currency_rk, data_actual_date)
);

DROP TABLE IF EXISTS DS.MD_EXCHANGE_RATE_D;
CREATE TABLE DS.MD_EXCHANGE_RATE_D (
    id integer,
    data_actual_date DATE not null,
    data_actual_end_date date,
    currency_rk integer not null,
    reduced_cource real,
    code_iso_num VARCHAR(3),
    PRIMARY KEY (id, data_actual_date, currency_rk)
);

DROP TABLE IF EXISTS DS.MD_LEDGER_ACCOUNT_S;
CREATE TABLE DS.MD_LEDGER_ACCOUNT_S (
    chapter CHAR(1),
    chapter_name VARCHAR(16),
    section_number INTEGER,
    section_name VARCHAR(22),
    subsection_name VARCHAR(21),
    ledger1_account INTEGER,
    ledger1_account_name VARCHAR(47),
    ledger_account INTEGER not null,
    ledger_account_name VARCHAR(153),
    characteristic CHAR(1),
    is_resident INTEGER,
    is_reserve INTEGER,
    is_reserved INTEGER,
    is_loan INTEGER,
    is_reserved_assets INTEGER,
    is_overdue INTEGER,
    is_interest INTEGER,
    pair_account VARCHAR, --VARCHAR(5),
    start_date DATE not null,
    end_date date,
    is_rub_only INTEGER,
    min_term VARCHAR(1),
    min_term_measure VARCHAR(1),
    max_term VARCHAR(1),
    max_term_measure VARCHAR(1),
    ledger_acc_full_name_translit VARCHAR(1),
    is_revaluation VARCHAR(1),
    is_correct VARCHAR(1),
    PRIMARY KEY (ledger_account, start_date)
);


CREATE SCHEMA IF NOT EXISTS DM;

DROP TABLE IF EXISTS DM.DM_ACCOUNT_TURNOVER_F;
CREATE TABLE DM.DM_ACCOUNT_TURNOVER_F (
    on_date DATE,
    account_rk integer,
    credit_amount real,
    credit_amount_rub real,
    debet_amount real,
    debet_amount_rub real
);

DROP TABLE IF EXISTS DM.DM_F101_ROUND_F;
CREATE TABLE DM.DM_F101_ROUND_F (
    FROM_DATE DATE,
    TO_DATE DATE,
    CHAPTER char(1),
    LEDGER_ACCOUNT char(5),
    CHARACTERISTIC char(1),
    BALANCE_IN_RUB real,
    R_BALANCE_IN_RUB real,
    BALANCE_IN_VAL real,
    R_BALANCE_IN_VAL real,
    BALANCE_IN_TOTAL real,
    R_BALANCE_IN_TOTAL real,
    TURN_DEB_RUB real,
    R_TURN_DEB_RUB real,
    TURN_DEB_VAL real,
    R_TURN_DEB_VAL real,
    TURN_DEB_TOTAL real,
    R_TURN_DEB_TOTAL real,
    TURN_CRE_RUB real,
    R_TURN_CRE_RUB real,
    TURN_CRE_VAL real,
    R_TURN_CRE_VAL real,
    TURN_CRE_TOTAL real,
    R_TURN_CRE_TOTAL real,
    BALANCE_OUT_RUB real,
    R_BALANCE_OUT_RUB real,
    BALANCE_OUT_VAL real,
    R_BALANCE_OUT_VAL real,
    BALANCE_OUT_TOTAL real,
    R_BALANCE_OUT_TOTAL real
);
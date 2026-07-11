CREATE TABLE IF NOT EXISTS raw_transactions (
    execution_id VARCHAR NOT NULL,
    source_file VARCHAR NOT NULL,
    source_row_number INTEGER NOT NULL,

    transaction_id VARCHAR,
    user_id VARCHAR,
    transaction_timestamp_raw VARCHAR,
    transaction_type VARCHAR,
    amount_raw VARCHAR,

    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (execution_id, source_row_number)
);

CREATE TABLE IF NOT EXISTS fact_transactions (
    execution_id VARCHAR NOT NULL,
    transaction_id VARCHAR NOT NULL,
    user_id VARCHAR NOT NULL,
    transaction_timestamp TIMESTAMP NOT NULL,
    transaction_type VARCHAR NOT NULL,
    amount DECIMAL(18, 2) NOT NULL,
    signed_amount DECIMAL(18, 2) NOT NULL,

    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (execution_id, transaction_id)
);

CREATE TABLE IF NOT EXISTS fact_user_balances (
    execution_id VARCHAR NOT NULL,
    user_id VARCHAR NOT NULL,
    balance DECIMAL(18, 2) NOT NULL,

    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (execution_id, user_id)
);

CREATE TABLE IF NOT EXISTS fact_pipeline_executions (
    execution_id VARCHAR NOT NULL,
    started_at TIMESTAMP NOT NULL,
    finished_at TIMESTAMP,
    duration_seconds DOUBLE,
    status VARCHAR NOT NULL,

    rows_read INTEGER NOT NULL DEFAULT 0,
    rows_valid INTEGER NOT NULL DEFAULT 0,
    rows_invalid INTEGER NOT NULL DEFAULT 0,
    rows_processed INTEGER NOT NULL DEFAULT 0,

    input_path VARCHAR,
    output_path VARCHAR,
    error_message VARCHAR,

    PRIMARY KEY (execution_id)
);

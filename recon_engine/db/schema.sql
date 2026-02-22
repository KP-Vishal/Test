CREATE TABLE IF NOT EXISTS raw_files (
    id BIGSERIAL PRIMARY KEY,
    recon_date DATE NOT NULL,
    source_file TEXT NOT NULL,
    rail TEXT NOT NULL,
    record_count INTEGER NOT NULL,
    checksum_sha256 TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bijlipay_transaction_base (
    id BIGSERIAL PRIMARY KEY,
    recon_date DATE NOT NULL,
    source_file TEXT NOT NULL,
    rail TEXT NOT NULL,
    rrn TEXT NOT NULL,
    tid TEXT,
    order_id TEXT,
    txn_date DATE NOT NULL,
    amount NUMERIC(18,2) NOT NULL,
    status TEXT NOT NULL,
    event_type TEXT NOT NULL,
    aggregator_id TEXT,
    institution_id TEXT,
    ack_enabled BOOLEAN,
    ack_received BOOLEAN,
    device_type TEXT,
    metadata JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS host_transaction_base (
    id BIGSERIAL PRIMARY KEY,
    recon_date DATE NOT NULL,
    source_file TEXT NOT NULL,
    rail TEXT NOT NULL,
    rrn TEXT NOT NULL,
    tid TEXT,
    order_id TEXT,
    txn_date DATE NOT NULL,
    amount NUMERIC(18,2) NOT NULL,
    status TEXT NOT NULL,
    event_type TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS transaction_errors (
    id BIGSERIAL PRIMARY KEY,
    recon_date DATE NOT NULL,
    source_file TEXT NOT NULL,
    rail TEXT NOT NULL,
    rrn TEXT NOT NULL,
    tid TEXT,
    order_id TEXT,
    txn_date DATE NOT NULL,
    error_code TEXT NOT NULL,
    error_message TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS adjustments (
    id BIGSERIAL PRIMARY KEY,
    recon_date DATE NOT NULL,
    source_file TEXT NOT NULL,
    rail TEXT NOT NULL,
    rrn TEXT NOT NULL,
    tid TEXT,
    order_id TEXT,
    txn_date DATE NOT NULL,
    original_payout_date DATE NOT NULL,
    amount NUMERIC(18,2) NOT NULL,
    adjustment_type TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS payouts (
    id BIGSERIAL PRIMARY KEY,
    recon_date DATE NOT NULL,
    source_file TEXT NOT NULL,
    rail TEXT NOT NULL,
    rrn TEXT NOT NULL,
    tid TEXT,
    order_id TEXT,
    txn_date DATE NOT NULL,
    amount NUMERIC(18,2) NOT NULL,
    payout_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS credit_validation (
    id BIGSERIAL PRIMARY KEY,
    recon_date DATE NOT NULL,
    source_file TEXT NOT NULL,
    rail TEXT NOT NULL,
    credit_date DATE NOT NULL,
    expected_amount NUMERIC(18,2) NOT NULL,
    credited_amount NUMERIC(18,2) NOT NULL,
    mismatch NUMERIC(18,2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_bijli_rrn ON bijlipay_transaction_base (rrn);
CREATE INDEX IF NOT EXISTS idx_bijli_tid ON bijlipay_transaction_base (tid);
CREATE INDEX IF NOT EXISTS idx_bijli_order_id ON bijlipay_transaction_base (order_id);
CREATE INDEX IF NOT EXISTS idx_bijli_txn_date ON bijlipay_transaction_base (txn_date);

CREATE INDEX IF NOT EXISTS idx_host_rrn ON host_transaction_base (rrn);
CREATE INDEX IF NOT EXISTS idx_host_tid ON host_transaction_base (tid);
CREATE INDEX IF NOT EXISTS idx_host_order_id ON host_transaction_base (order_id);
CREATE INDEX IF NOT EXISTS idx_host_txn_date ON host_transaction_base (txn_date);

CREATE INDEX IF NOT EXISTS idx_errors_rrn ON transaction_errors (rrn);
CREATE INDEX IF NOT EXISTS idx_errors_tid ON transaction_errors (tid);
CREATE INDEX IF NOT EXISTS idx_errors_order_id ON transaction_errors (order_id);
CREATE INDEX IF NOT EXISTS idx_errors_txn_date ON transaction_errors (txn_date);

CREATE INDEX IF NOT EXISTS idx_adjustments_rrn ON adjustments (rrn);
CREATE INDEX IF NOT EXISTS idx_adjustments_tid ON adjustments (tid);
CREATE INDEX IF NOT EXISTS idx_adjustments_order_id ON adjustments (order_id);
CREATE INDEX IF NOT EXISTS idx_adjustments_txn_date ON adjustments (txn_date);

CREATE INDEX IF NOT EXISTS idx_payouts_rrn ON payouts (rrn);
CREATE INDEX IF NOT EXISTS idx_payouts_tid ON payouts (tid);
CREATE INDEX IF NOT EXISTS idx_payouts_order_id ON payouts (order_id);
CREATE INDEX IF NOT EXISTS idx_payouts_txn_date ON payouts (txn_date);

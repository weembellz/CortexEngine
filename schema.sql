CREATE TABLE IF NOT EXISTS orders (
    id TEXT PRIMARY KEY,
    item_type TEXT NOT NULL,
    tx_hash TEXT,
    xmr_amount REAL DEFAULT 0.04,
    timestamp INTEGER
);
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT,
    message TEXT,
    timestamp INTEGER
);

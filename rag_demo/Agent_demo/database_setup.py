import sqlite3

DB_NAME = "enterprise_ai.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# ------------------------------------------------
# INTEGRATIONS
# ------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS integrations (
    integration_id INTEGER PRIMARY KEY,
    integration_name TEXT NOT NULL,
    application TEXT NOT NULL,
    status TEXT NOT NULL,
    environment TEXT NOT NULL,
    last_run_time TEXT
)
""")

# ------------------------------------------------
# INTEGRATION ERRORS
# ------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS integration_errors (
    error_id INTEGER PRIMARY KEY,
    integration_id INTEGER,
    error_type TEXT,
    error_message TEXT,
    error_time TEXT,
    FOREIGN KEY (integration_id)
        REFERENCES integrations(integration_id)
)
""")

# ------------------------------------------------
# CUSTOMERS
# ------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    region TEXT
)
""")

# ------------------------------------------------
# SALES
# ------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    sales_id TEXT PRIMARY KEY,
    customer_id TEXT,
    amount REAL,
    sales_date TEXT,
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
)
""")

conn.commit()

print("Database created successfully.")
print(f"Database: {DB_NAME}")

conn.close()
import sqlite3

DB_NAME = "enterprise_ai.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# -------------------------------
# Integrations
# -------------------------------

integrations = [
    (1001, "InvoiceSync", "Oracle Fusion", "FAILED", "PROD", "2026-08-20 10:30"),
    (1002, "CustomerSync", "Oracle Fusion", "SUCCESS", "PROD", "2026-08-20 10:35"),
    (1003, "OrderSync", "Oracle EBS", "FAILED", "UAT", "2026-08-20 11:00"),
    (1004, "PaymentSync", "Oracle Fusion", "RUNNING", "PROD", "2026-08-20 11:15"),
    (1005, "ShipmentSync", "Oracle EBS", "FAILED", "PROD", "2026-08-20 11:30")
]

cursor.executemany("""
INSERT OR IGNORE INTO integrations
VALUES (?, ?, ?, ?, ?, ?)
""", integrations)


# -------------------------------
# Errors
# -------------------------------

errors = [
    (501, 1001, "AUTHENTICATION",
     "OAuth token expired", "2026-08-20 10:30"),

    (502, 1003, "DATABASE",
     "Database connection timeout", "2026-08-20 11:00"),

    (503, 1005, "API",
     "External API returned HTTP 500", "2026-08-20 11:30")
]

cursor.executemany("""
INSERT OR IGNORE INTO integration_errors
VALUES (?, ?, ?, ?, ?)
""", errors)


# -------------------------------
# Customers
# -------------------------------

customers = [
    ("C100", "ABC Ltd", "India"),
    ("C101", "XYZ Corp", "USA"),
    ("C102", "PQR Ltd", "UK")
]

cursor.executemany("""
INSERT OR IGNORE INTO customers
VALUES (?, ?, ?)
""", customers)


# -------------------------------
# Sales
# -------------------------------

sales = [
    ("S001", "C100", 125000, "2026-08-18"),
    ("S002", "C100", 85000, "2026-08-19"),
    ("S003", "C101", 250000, "2026-08-19"),
    ("S004", "C102", 175000, "2026-08-20")
]

cursor.executemany("""
INSERT OR IGNORE INTO sales
VALUES (?, ?, ?, ?)
""", sales)

conn.commit()

print("Enterprise data inserted successfully.")

conn.close()
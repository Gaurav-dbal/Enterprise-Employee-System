import sqlite3

DB_NAME = "enterprise_ai.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

print("\n==========================================")
print("       ENTERPRISE AI DATABASE")
print("==========================================")

# 1. Show all integrations
print("\n--- ALL INTEGRATIONS ---")

cursor.execute("""
SELECT *
FROM integrations
""")

rows = cursor.fetchall()

for row in rows:
    print(row)


# 2. Show failed integrations
print("\n--- FAILED INTEGRATIONS ---")

cursor.execute("""
SELECT integration_id,
       integration_name,
       status,
       environment
FROM integrations
WHERE status = 'FAILED'
""")

rows = cursor.fetchall()

for row in rows:
    print(row)


# 3. Show error for integration 1001
print("\n--- ERROR FOR INTEGRATION 1001 ---")

cursor.execute("""
SELECT error_type,
       error_message,
       error_time
FROM integration_errors
WHERE integration_id = 1001
""")

rows = cursor.fetchall()

for row in rows:
    print(row)


# 4. Total sales for C100
print("\n--- TOTAL SALES FOR C100 ---")

cursor.execute("""
SELECT SUM(amount)
FROM sales
WHERE customer_id = 'C100'
""")

result = cursor.fetchone()

print("Total Sales:", result[0])


conn.close()
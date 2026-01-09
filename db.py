import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS scans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    barcode TEXT,
    type TEXT,
    name TEXT, 
    surname TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()
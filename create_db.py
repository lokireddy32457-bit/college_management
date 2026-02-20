import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    rollno TEXT,
    branch TEXT,
    year TEXT
)
""")

cur.execute("SELECT * FROM admin WHERE username='admin'")
if not cur.fetchone():
    cur.execute("INSERT INTO admin VALUES (NULL,'admin','admin123')")

conn.commit()
conn.close()

print("Database created successfully")

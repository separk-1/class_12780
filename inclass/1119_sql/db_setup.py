import sqlite3
# Connect to SQLite database (or create it)
conn = sqlite3.connect("construction_project.db")
cursor = conn.cursor()
# Create tables with lowercase column names and "id" as primary keys
cursor.execute('''CREATE TABLE IF NOT EXISTS workers (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
role TEXT,
contact TEXT
)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS materials (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
quantity INTEGER,
cost REAL
)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
id INTEGER PRIMARY KEY,
description TEXT NOT NULL,
deadline DATE,
assigned_worker_id INTEGER,
FOREIGN KEY (assigned_worker_id) REFERENCES workers (id)
)''')
print("Tables created successfully!")
conn.commit()
conn.close()

import sqlite3

conn = sqlite3.connect("construction_project.db")
cursor = conn.cursor()
# Insert sample data
cursor.execute("INSERT INTO workers (name, role, contact) VALUES (?, ?, ?)",
('alice', 'engineer', 'alice@example.com'))
cursor.execute("INSERT INTO workers (name, role, contact) VALUES (?, ?, ?)",
('bob', 'foreman', 'bob@example.com'))
cursor.execute("INSERT INTO materials (name, quantity, cost) VALUES (?, ?, ?)",
('cement', 500, 1200.50))
cursor.execute("INSERT INTO materials (name, quantity, cost) VALUES (?, ?, ?)",
('steel', 300, 2500.00))
cursor.execute("INSERT INTO tasks (description, deadline, assigned_worker_id) VALUES (?, ?, ?)",
('foundation work', '2024-12-01', 1))
cursor.execute("INSERT INTO tasks (description, deadline, assigned_worker_id) VALUES (?, ?, ?)",
('pillar construction', '2025-01-15', 2))
conn.commit()
print("Sample data inserted successfully!")
conn.close()

import sqlite3

conn = sqlite3.connect("construction_project.db")
cursor = conn.cursor()
# Join tasks with workers
print("\nTasks with assigned workers:")
cursor.execute('''SELECT tasks.description, workers.name
FROM tasks
JOIN workers ON tasks.assigned_worker_id = workers.id''')
for row in cursor.fetchall():
    print(row)
conn.close()

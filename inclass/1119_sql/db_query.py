import sqlite3

conn = sqlite3.connect("construction_project.db")
cursor = conn.cursor()
# List all workers
print("Workers:")
cursor.execute("SELECT * FROM workers")
for row in cursor.fetchall():
    print(row)
# Total cost of materials
cursor.execute("SELECT SUM(cost) AS total_cost FROM materials")
total_cost = cursor.fetchone()[0]
print(f"\nTotal Cost of Materials: {total_cost}")
# Tasks assigned to a specific worker
worker_id = 1 # Example: Alice
print("\nTasks assigned to worker ID 1:")
cursor.execute("SELECT * FROM tasks WHERE assigned_worker_id = ?", (worker_id,))
for row in cursor.fetchall():
    print(row)
conn.close()

'''
name: Seongeun Park
andrewID: seongeup
course number: 12-780
homework number: HW4
exercise 3

'''
import sqlite3

# Connect to the SQLite database
db_path = 'bridges.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

river_names = cursor.fetchall()

print("Distinct river names in database:")
for river in river_names:
    print(river[0])
# Query 1: Names and locations of all bridges over the Monongahela that are still standing
query_monongahela = '''
SELECT bridge_name, mile
FROM Bridges
WHERE river = 'M' AND (demolished IS NULL OR demolished = 0)
'''
cursor.execute(query_monongahela)
monongahela_bridges = cursor.fetchall()

print("Bridges over the Monongahela that are still standing:")
for name, mile in monongahela_bridges:
    print(f"Name: {name}, Location (Mile): {mile}")

# Query 2: Names and locations of all arch bridges made of steel
query_arch_steel = '''
SELECT bridge_name, mile
FROM Bridges b
JOIN BridgeTypes bt ON b.bridge_type_id = bt.bridge_type_id
WHERE bt.type = 'arch' AND b.material = 'Steel'
'''
cursor.execute(query_arch_steel)
arch_steel_bridges = cursor.fetchall()

print("\nArch bridges made of steel:")
for name, mile in arch_steel_bridges:
    print(f"Name: {name}, Location (Mile): {mile}")

# Close the database connection
conn.close()
'''
name: Seongeun Park
andrewID: seongeup
course number: 12-780
homework number: HW4
exercise 5

'''
import sqlite3
import pandas as pd

# Connect to the SQLite database
db_path = 'bridges.db'
conn = sqlite3.connect(db_path)

# Step 1: Join Bridges and BridgeTypes tables to extract required columns
query = '''
SELECT 
    bt.type AS Type,
    bt.subtype AS Subtype,
    b.pattern AS Pattern,
    b.material AS Material
FROM Bridges b
JOIN BridgeTypes bt
ON b.bridge_type_id = bt.bridge_type_id
'''
df = pd.read_sql_query(query, conn)

# Step 2: Remove duplicates (if needed) to create a clean BridgeType table
bridge_type_table = df.drop_duplicates().reset_index(drop=True)

# Step 3: Create a new table for bridge types in the database
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS NewBridgeType (
    type TEXT NOT NULL,
    subtype TEXT NOT NULL,
    pattern TEXT,
    material TEXT
)
''')

# Step 4: Insert data into the new table
bridge_type_data = bridge_type_table.values.tolist()
cursor.executemany('INSERT INTO NewBridgeType VALUES (?, ?, ?, ?)', bridge_type_data)

# Commit changes and close the connection
conn.commit()
conn.close()

# Save the cleaned bridge type table to a CSV file (optional)
output_path = 'NewBridgeType.csv'
bridge_type_table.to_csv(output_path, index=False)
print(f"NewBridgeType table created successfully and saved to '{output_path}'.")
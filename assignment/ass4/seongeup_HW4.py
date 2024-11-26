'''
name: Seongeun Park
andrewID: seongeup
course number: 12-780
homework number: HW4
'''

# Question 1

import pandas as pd
import sqlite3

# Load the Excel file using xlrd engine
file_path = 'PittsburghBridges.xls'
df = pd.read_excel(file_path, engine="xlrd", header=None)

# Displaying the first few rows for inspection
print("Original Data:")
print(df.head())

# Step 1: Remove completely empty rows
df_cleaned = df.dropna(how="all")

# Step 2: Remove unnecessary spaces from all string columns and normalize spaces
df_cleaned = df_cleaned.applymap(
    lambda x: " ".join(x.split()) if isinstance(x, str) else x
)

# Step 3: Remove the first two rows and use the third row as column names
df_cleaned.columns = df_cleaned.iloc[2]  # Set the third row as column names
df_cleaned = df_cleaned.iloc[3:]  # Drop the first three rows (including the header row)

# Step 4: Remove rows with missing values in critical columns ('Type', 'Subtype')
if 'Type' in df_cleaned.columns and 'Subtype' in df_cleaned.columns:
    df_cleaned = df_cleaned.dropna(subset=['Type', 'Subtype'])  # Remove rows with NaN in 'Type' or 'Subtype'
    df_cleaned = df_cleaned[df_cleaned['Type'].str.strip() != '']  # Remove rows with empty 'Type'
    df_cleaned = df_cleaned[df_cleaned['Subtype'].str.strip() != '']  # Remove rows with empty 'Subtype'

# Reset index for cleaned data
df_cleaned.reset_index(drop=True, inplace=True)

# Displaying cleaned data
print("\nCleaned Data:")
print(df_cleaned.head())

# Save the cleaned dataset to a CSV for further inspection or use
output_path = 'PittsburghBridges_Cleaned.csv'
df_cleaned.to_csv(output_path, index=False)

print(f"Data cleaning completed. Cleaned data saved to '{output_path}'.")

# Question 2 & 4
# Load the cleaned CSV file
file_path = 'PittsburghBridges_Cleaned.csv'
df = pd.read_csv(file_path)

# Extract unique bridge types and create the BridgeTypes table
bridge_types = df[['Type', 'Subtype']].drop_duplicates().reset_index(drop=True)
bridge_types['bridge_type_id'] = bridge_types.index + 1  # Add unique ID for each type

# Add a foreign key to the original dataframe
df = pd.merge(df, bridge_types, on=['Type', 'Subtype'], how='left')

# Connect to SQLite database (or create one)
conn = sqlite3.connect('bridges.db')
cursor = conn.cursor()

# Create the BridgeTypes table
cursor.execute('''
CREATE TABLE BridgeTypes (
    bridge_type_id INTEGER PRIMARY KEY,
    type TEXT NOT NULL,
    subtype TEXT
)
''')

# Create the Bridges table
cursor.execute('''
CREATE TABLE Bridges (
    bridge_id INTEGER PRIMARY KEY,
    bridge_name TEXT NOT NULL,
    river TEXT,
    mile REAL,
    erected INTEGER,
    demolished INTEGER,
    description TEXT,
    pattern TEXT,
    aqueduct TEXT,
    main_span REAL,
    num_spans INTEGER,
    length REAL,
    material TEXT,
    owner TEXT,
    designer TEXT,
    iils_id INTEGER,
    bridge_type_id INTEGER,
    FOREIGN KEY (bridge_type_id) REFERENCES BridgeTypes (bridge_type_id)
)
''')

# Insert data into BridgeTypes table
bridge_types_data = bridge_types[['bridge_type_id', 'Type', 'Subtype']].values.tolist()
cursor.executemany('INSERT INTO BridgeTypes VALUES (?, ?, ?)', bridge_types_data)

# Insert data into Bridges table
bridges_data = df[['Bridge#', 'Name', 'River', 'Mile', 'Erected', 'Demolished', 'Description', 'Pattern', 'Aqueduct',
                   'Main Span', '# Spans', 'Length', 'Material', 'Owner', 'Designer', 'iils #', 'bridge_type_id']].values.tolist()
cursor.executemany('''
INSERT INTO Bridges (
    bridge_id, bridge_name, river, mile, erected, demolished, description, pattern, aqueduct, main_span, 
    num_spans, length, material, owner, designer, iils_id, bridge_type_id
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', bridges_data)

# Commit and close the connection
conn.commit()
conn.close()

print("Database created successfully with BridgeTypes and Bridges tables.")

# Question 3
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

# Question 5
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
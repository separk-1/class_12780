'''
name: Seongeun Park
andrewID: seongeup
course number: 12-780
homework number: HW4
exercise 2

'''

import pandas as pd
import sqlite3

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
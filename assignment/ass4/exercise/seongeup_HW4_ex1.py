'''
name: Seongeun Park
andrewID: seongeup
course number: 12-780
homework number: HW4
exercise 1

I used Pandas to clean data
Step 1: Remove completely empty rows
Step 2: Remove unnecessary spaces from all string columns
Step 3: Remove the first two rows and use the third row as column names
Step 4: Remove rows with missing values in critical columns ('Type', 'Subtype')
'''
import pandas as pd

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
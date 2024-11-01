# Name: Seongeun Park
# AndrewID: seongeup
# Course Number: 12-780
# HW 1
# exercise 1, 2, 3, 4

# exercise 1
import numpy as np
import csv
import pandas as pd

with open('AlleghenyCountyAssets.csv', 'r') as file:
    reader = csv.reader(file)
    data = np.array([row for row in reader])

# print(data[:5])

# exercise 2
asset_dict = {}

for row in data[1:]:  
    asset_name = row[1]
    parcel_id = row[0] if row[0] else 'UNKNOWN'
    asset_dict[asset_name] = parcel_id

# print(dict(list(asset_dict.items())[:5]))

# exercise 3
asset_count = {} 

for row in data[1:]:
    asset_type = row[2] 

    if asset_type in asset_count:
        asset_count[asset_type] += 1
    else:
        asset_count[asset_type] = 1

for asset_type, count in asset_count.items():
    print(f"{asset_type}: {count}")

# exercise 4
df = pd.DataFrame(list(asset_count.items()), columns=['Asset Type', 'Count'])

print(df)
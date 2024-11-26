import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# 1. Load data
# Polling places data
polling_places = gpd.read_file("polling_places.geojson")

# Voting district boundaries
voting_districts = gpd.read_file("voting_bounds.geojson")

# Census block group map (load GeoJSON from ZIP)
block_groups = gpd.read_file("zip://tl_2024_42_bg.zip")

# Census block group population data
population_data = pd.read_csv("ACSDT5Y2022.B01003-Data.csv")

# 2. Clean and preprocess the population data
# Extract GEO_ID to match the block group GEOID format
population_data["GEOID"] = population_data["GEO_ID"].str.split("US").str[-1]  # Extract ID after "US"
population_data = population_data[["GEOID", "B01003_001E"]]  # Keep relevant columns only
population_data["B01003_001E"] = pd.to_numeric(population_data["B01003_001E"], errors="coerce")  # Ensure numeric values

# 3. Reproject to a projected CRS (e.g., UTM Zone 17N for Allegheny County)
polling_places = polling_places.to_crs(epsg=32617)  # UTM Zone 17N
block_groups = block_groups.to_crs(epsg=32617)

# 4. Create a 1.5km buffer around polling places
polling_places["buffer"] = polling_places.geometry.buffer(1500)  # 1.5km radius
polling_buffers = gpd.GeoDataFrame(polling_places, geometry="buffer", crs=polling_places.crs)

# 5. Use spatial join to check block groups outside buffers
# Perform a spatial join to find intersecting block groups
intersecting = gpd.sjoin(block_groups, polling_buffers, predicate='intersects', how='inner')

# Filter block groups that are outside the buffers
outside_block_groups = block_groups.loc[~block_groups.index.isin(intersecting.index)]

# 6. Merge population data with block groups outside the buffer
outside_block_groups["GEOID"] = outside_block_groups["GEOID"].astype(str)
outside_population = outside_block_groups.merge(population_data, on="GEOID")

# 7. Calculate total population outside the buffer
total_outside_population = outside_population["B01003_001E"].sum()

# 8. Print the result
print(f"Number of voters more than 15 minutes walking distance (1.5km) from their polling place: {int(total_outside_population)}")
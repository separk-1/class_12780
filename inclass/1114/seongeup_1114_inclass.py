import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import datetime

# Step 1: Load and Explore Data
# Load a sample rainfall dataset

data = pd.read_csv('synthetic_rainfall_data.csv', parse_dates=['Date'])

data['Rainfall'] = ((data['Sensor 1 Rainfall (mm)'] + data['Sensor 2 Rainfall (mm)'])/2)

# Step 3: Calculate Annual Maximum Rainfall
# Extract the year from the 'Date' column
data['Year'] = data['Date'].dt.year

# Find the maximum rainfall for each year
annual_max = data.groupby('Year')['Rainfall'].min()


# Step 4: Rank-Based Frequency Analysis for 10-Year and 100-Year Storms
# Sort the annual maximum rainfall values in descending order
def get_sorted_annual_max(data):
    """
    Sorts annual maximum rainfall values in descending order using a DIY sorting algorithm (bubble sort)
    and resets the index.

    Parameters:
    - data (pd.Series): A pandas Series of annual maximum rainfall values.

    Returns:
    - pd.DataFrame: Sorted rainfall values with the index reset as a DataFrame.
    """
    # Convert Series to a list of values to perform sorting
    rainfall_values = data.tolist()
    
    # Bubble sort algorithm to sort values in descending order
    n = len(rainfall_values)
    for i in range(n):
        for j in range(0, n - i - 1):
            if rainfall_values[j] < rainfall_values[j + 1]:  # Swap if the next item is greater
                rainfall_values[j], rainfall_values[j + 1] = rainfall_values[j + 1], rainfall_values[j]

    # Convert the sorted list back to a DataFrame with reset index
    sorted_data = pd.DataFrame(rainfall_values, columns=['Rainfall'])
    return sorted_data

sorted_annual_max = get_sorted_annual_max(annual_max) 

# Calculate rank for each sorted value
sorted_annual_max['Rank'] = np.arange(1, len(sorted_annual_max)+1)

# Calculate probability of exceedance (using Weibull plotting position)
sorted_annual_max['AEP'] = sorted_annual_max['Rank'] / (len(sorted_annual_max) + 1)


# Step 5: Determine 10-Year and 100-Year Rainfall Events
# A 10-year event has an AEP of 10%, and a 100-year event has an AEP of 1%
rainfall_10yr = sorted_annual_max[sorted_annual_max['AEP'] <= 0.1]['Rainfall'].iloc[-1]
rainfall_100yr = sorted_annual_max[sorted_annual_max['AEP'] <= 0.01]['Rainfall'].iloc[-1]

print(f"Estimated 10-Year Rainfall Event: {rainfall_10yr} mm")
print(f"Estimated 100-Year Rainfall Event: {rainfall_100yr} mm")

# Step 6: Plotting the Exceedance Curve
plt.figure(figsize=(10, 6))
plt.plot(sorted_annual_max['AEP'], sorted_annual_max['Rainfall'], marker='o', linestyle='-')
plt.axhline(y=rainfall_10yr, color='r', linestyle='--', label="10-Year Storm")
plt.axhline(y=rainfall_100yr, color='b', linestyle='--', label="100-Year Storm")

plt.yscale('log')
plt.gca().invert_xaxis()  # Invert x-axis for exceedance probability
plt.xlabel('Annual Exceedance Probability (AEP)')
plt.ylabel('Rainfall (mm)')
plt.title('Exceedance Probability Curve')
plt.legend()
plt.grid(True)
plt.show()

# Step 7a: Simple Flood Risk Assessment
# Here we can assume infrastructure capacity and compare against 10-year and 100-year storm values
# Assuming a basic drainage capacity (e.g., 50 mm in a day)
drainage_capacity = 50  # mm/day

if rainfall_10yr > drainage_capacity:
    print("Infrastructure may need upgrades to handle 10-year storm.")
else:
    print("Infrastructure is likely sufficient for a 10-year storm.")

if rainfall_100yr > drainage_capacity:
    print("Infrastructure may need significant upgrades to handle a 100-year storm.")
else:
    print("Infrastructure is likely sufficient for a 100-year storm.")

# Step 7b: Enhanced Flood Risk Assessment for New Neighborhood Development
# Define runoff coefficients for surfaces before and after development
# Before development: mostly permeable (e.g., grass)
# After development: mix of impermeable surfaces (pavement, rooftops) and permeable surfaces (grass)
runoff_coefficients_before = {
    "grass": 0.3
}

runoff_coefficients_after = {
    "pavement": 0.9,    # Impermeable surfaces, e.g., pavement or rooftops
    "grass": 0.3        # Remaining permeable areas like landscaping or parks
}

# Define the proportions of each surface type after development
area_proportions_before = {"grass": 1.0}  # 100% permeable before development
area_proportions_after = {"pavement": 0.7, "grass": 0.3}  # 70% impermeable, 30% permeable

# Assume drainage area in square meters (example: 1,000 square meters)
drainage_area = 1000  # m^2


# Function to calculate runoff volume for each scenario
def calculate_total_runoff(rainfall, area, coefficients, proportions):
    total_runoff = 0
    for surface, coefficient in coefficients.items():
        proportion = proportions.get(surface, 0) 
        surface_area = area * proportion
        total_runoff += calculate_runoff(rainfall, surface_area, coefficient)
    return total_runoff

def calculate_runoff(rainfall, area, coefficient): 
    """
    Calculate runoff volume in cubic meters.

    Parameters:
    - rainfall (float): Rainfall in millimeters.
    - area (float): Surface area in square meters.
    - coefficient (float): Runoff coefficient (dimensionless).

    Returns:
    - float: Runoff volume in cubic meters.
    """
    # Convert rainfall from millimeters to meters (by dividing by 1000),
    # then multiply by area and coefficient to get runoff volume.
    runoff_volume = (rainfall / 1000) * area * coefficient
    return runoff_volume

# Calculate runoff volumes for 10-year and 100-year storms before and after development
rainfall_events = {"10-year": rainfall_10yr, "100-year": rainfall_100yr}
for event_name, rainfall in rainfall_events.items():
    runoff_before = calculate_total_runoff(rainfall, drainage_area, runoff_coefficients_before, area_proportions_before)
    runoff_after = calculate_total_runoff(rainfall, drainage_area, runoff_coefficients_after, area_proportions_after)
    
    print(f"\n{event_name.capitalize()} Storm:")
    print(f"Runoff Before Development: {runoff_before:.2f} cubic meters")
    print(f"Runoff After Development: {runoff_after:.2f} cubic meters")
    
    # Compare runoff volume to drainage capacity
    drainage_capacity_volume = drainage_capacity / 1000 * drainage_area  # mm to meters conversion
    
    if runoff_before > drainage_capacity_volume: 
        print("Before development: Drainage system may need upgrades.")
    else:
        print("Before development: Drainage system is likely sufficient.")
    
    if runoff_after > drainage_capacity_volume:
        print("After development: Drainage system may need significant upgrades." )
    else:
        print("After development: Drainage system is likely sufficient.")


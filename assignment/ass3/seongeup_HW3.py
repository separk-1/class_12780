'''
name: Seongeun Park
andrewID: seongeup
course number: 12-780
homework number: HW3
'''

import pandas as pd
import tkinter as tk
from tkinter import ttk

# Step 1: Read the CSV file into a DataFrame
data = pd.read_csv("AlleghenyCountyAssets.csv")

# Step 2: Filter the data to get the first instance of each unique tag, excluding blank and NaN tags
filtered_data = data.dropna(subset=['tags'])  # Remove rows with NaN tags in 'tags'
filtered_data = filtered_data[filtered_data['tags'] != '']  # Remove blank tags
unique_tags = filtered_data.groupby('tags').first().reset_index()  # Get the first instance for each unique tag
result_data = unique_tags[['parcel_id', 'name', 'tags', 'city']]  # Select relevant columns

# Step 2 Output: Print the result in the terminal
print(result_data)

# Step 3: Display the data in a GUI window
def show_table():
    root = tk.Tk()
    root.title("Allegheny County Assets - Unique Tags")

    # Create a Treeview to display the data
    tree = ttk.Treeview(root, columns=('parcel_id', 'name', 'tags', 'city'), show='headings')
    tree.heading('parcel_id', text='Parcel ID')
    tree.heading('name', text='Name')
    tree.heading('tags', text='Tag')
    tree.heading('city', text='City')

    # Insert data into the Treeview
    for _, row in result_data.iterrows():
        tree.insert('', tk.END, values=row.tolist())

    tree.pack(expand=True, fill='both')

    # Add a quit button
    quit_button = ttk.Button(root, text="Quit", command=root.destroy)
    quit_button.pack()

    root.mainloop()

# Show the GUI window
show_table()

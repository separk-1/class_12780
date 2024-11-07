import tkinter as tk

def calculate(*args):
    try:
        value = float(feet.get())
        meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass

# YOUR CODE HERE v
root = tk.Tk()
root.title("Feet to meters")
mainframe=tk.Frame(root)
mainframe.grid(column=0, row=0)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
feet=tk.StringVar()
feet_entry=tk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1)
meters=tk.StringVar()
tk.Label(mainframe, textvariable=meters).grid(column=2,row=2)
tk.Button(mainframe, text="calculate", command=calculate).grid(column=3, row=3)
tk.Label(mainframe, text="feet").grid(column=3, row=1)
tk.Label(mainframe, text="is equivalent to").grid(column=1, row=2)
tk.Label(mainframe, text="meters").grid(column=3, row=2)
#YOUR CODE HERE

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)
# feet_entry.focus()
root.bind("<Return>", calculate)
root.mainloop()


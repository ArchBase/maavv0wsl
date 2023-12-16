import tkinter as tk
from tkinter import filedialog
import subprocess

def run_admin_file():
    file_path = "admin.py"
    if file_path:
        subprocess.Popen(["python3", file_path])
        root.after(100, root.destroy)  # Close the Tkinter application after a short delay

def run_client_file():
    file_path = "client_stylized.py"
    if file_path:
        subprocess.Popen(["python3", file_path])
        root.after(100, root.destroy)  # Close the Tkinter application after a short delay


# Create the main window
root = tk.Tk()
root.title("____maav____")
root.geometry("400x300")

# Create a button to choose and run a Python file
button = tk.Button(root, text="Train model", command=run_admin_file)
button.pack(padx=10, pady=10)

# Create a button to choose and run a Python file
button = tk.Button(root, text="Use model", command=run_client_file)
button.pack(padx=10, pady=10)


# Start the Tkinter event loop
root.mainloop()

import tkinter as tk
from tkinter import ttk
import threading
import time

def start_progress():
    # Start a new thread for the progress bar
    progress_thread = threading.Thread(target=update_progress)
    progress_thread.start()

def update_progress():
    for i in range(101):
        time.sleep(0.1)  # Simulate a time-consuming task
        progress_bar["value"] = i
        root.update_idletasks()  # Update the GUI
    progress_bar["value"] = 0

def stop_progress():
    progress_bar["value"] = 0  # Reset the progress bar

def get_text_input():
    text_content = text_input.get("1.0", tk.END)  # Get the content from the text input field
    print("Text Input Content:")
    print(text_content)

def process_number():
    try:
        number = int(number_entry.get())
        number_label.config(text=f"Entered Number: {number}")
    except ValueError:
        number_label.config(text="Invalid input. Enter a valid number.")

# Create the main window
root = tk.Tk()
root.title("GUI Application")

# Create three buttons
start_button = tk.Button(root, text="Start Progress", command=start_progress)
stop_button = tk.Button(root, text="Stop Progress", command=stop_progress)
get_text_button = tk.Button(root, text="Get Text Input", command=get_text_input)

# Create a progress bar in determinate mode
progress_bar = ttk.Progressbar(root, mode="determinate")

# Create a multiline text input field
text_input = tk.Text(root, height=10, width=40)

# Create a label and entry for accepting numbers
number_label = tk.Label(root, text="Enter a Number:")
number_entry = tk.Entry(root)
process_number_button = tk.Button(root, text="Process Number", command=process_number)

# Place widgets on the grid
start_button.grid(row=0, column=0, padx=5, pady=5)
stop_button.grid(row=0, column=1, padx=5, pady=5)
get_text_button.grid(row=0, column=2, padx=5, pady=5)
progress_bar.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
text_input.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
number_label.grid(row=3, column=0, padx=5, pady=5)
number_entry.grid(row=3, column=1, padx=5, pady=5)
process_number_button.grid(row=3, column=2, padx=5, pady=5)

# Start the Tkinter event loop
root.mainloop()

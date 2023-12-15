import maav
import tkinter as tk
from tkinter import scrolledtext
import threading

transformer = maav.Transformer(load_from_file=True)

def on_button_click():
    out_widget.delete("1.0", tk.END)  # Clear existing text
    out_widget.insert(tk.END, (transformer.generate_response(in_widget.get("1.0", tk.END)))[0])  # Insert new text

def run_on_thread():
    thread = threading.Thread(target=on_button_click)
    thread.start()

# Create the main window
root = tk.Tk()
root.title("Model Client")

# Create a text widget
in_label = tk.Label(root, text="Input your query:")
in_label.pack()
in_widget = scrolledtext.ScrolledText(root, width=40, height=10)
in_widget.pack(padx=10, pady=10)

# Create a text widget
out_label = tk.Label(root, text="Output of query:")
out_widget = scrolledtext.ScrolledText(root, width=40, height=10)
out_label.pack()
out_widget.pack(padx=10, pady=10)


# Create a button
button = tk.Button(root, text="Generate Response", command=run_on_thread)
button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()

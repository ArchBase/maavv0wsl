import maav
import tkinter as tk
from tkinter import ttk
import threading

stop = False
transformer = None
load_from_file=False

def start_training():
    status_label.config(text="Initializing training")
    # Start a new thread for the progress bar
    progress_thread = threading.Thread(target=update_progress)
    progress_thread.start()

def update_progress():
    global load_from_file
    global transformer
    try:
        # initialize
        epochs = int(epoch_entry.get())
        epochs_per_step = int(strength_entry.get())
        width = int(width_entry.get())
        transformer = maav.Transformer(load_from_file, dataset_length=width)
        # process
        status_label.config(text="Training started")
        for i in range(epochs):
            if not stop:
                percent = (i/epochs)*100
                progress_bar['value'] = percent
                percent_label.config(text=(str(round(percent, 2)) + "%"))
                transformer.bake_model_step_by_step(epochs=epochs_per_step)
                root.update_idletasks()
            else:
                break
        progress_bar['value'] = 0
        status_label.config(text="Training complete")

    except ValueError:
        status_label.config(text="Please fill all the fields")
        print("Please fill all the fields")
def start_training_existing():
    load_from_file = True
    status_label.config(text="Loaded existing model")
def stop_progress():
    global stop
    stop = True

def save():
    status_label.config(text="Saving the model")
    progress_thread = threading.Thread(target=transformer.save(status_label))
    progress_thread.start()

# Create the main window
root = tk.Tk()
root.title("Model Trainer")

# Create three buttons
start_button = tk.Button(root, text="Start Training", command=start_training)
existing_button = tk.Button(root, text="Load Existing model", command=start_training_existing)
stop_button = tk.Button(root, text="Stop Progress", command=stop_progress)
get_text_button = tk.Button(root, text="Save Model", command=save)

# Create a progress bar in determinate mode

progress_bar = ttk.Progressbar(root, mode="determinate", length=500)

# Place widgets on the grid
start_button.grid(row=0, column=0, padx=5, pady=5)
stop_button.grid(row=0, column=1, padx=5, pady=5)
existing_button.grid(row=0, column=3, padx=5, pady=5)
get_text_button.grid(row=0, column=2, padx=5, pady=5)
progress_bar.grid(row=1, column=0, columnspan=3, padx=5, pady=5)


percent_label = tk.Label(root, text="")
percent_label.grid(row=1, column=2)

epoch_label = tk.Label(root, text="Enter epochs")
epoch_label.grid(row=2, column=0)
epoch_entry = tk.Entry(root)
epoch_entry.grid(row=2, column=1)

strength_label = tk.Label(root, text="Enter epoches per step:")
strength_label.grid(row=4, column=0)
strength_entry = tk.Entry(root)
strength_entry.grid(row=4, column=1)

# Create a label for displaying status
status_label = tk.Label(root, text="Ready", bd=1, fg="red")


width_label = tk.Label(root, text="Datset width:")
width_label.grid(row=3, column=0)
width_entry = tk.Entry(root)
width_entry.grid(row=3, column=1)

status_label.grid(row=5, column=0)

# Start the Tkinter event loop
root.mainloop()

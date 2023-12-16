import maav
import tkinter as tk
from tkinter import Scrollbar, Text, Entry, END
transformer = maav.Transformer(load_from_file=True)
class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("One-to-One Chat")
        
        # Create Text widget to display messages
        self.messages_frame = Text(root, wrap="word")
        self.messages_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Add a scrollbar to the Text widget
        scrollbar = Scrollbar(self.messages_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Attach the Text widget to the scrollbar
        self.messages_frame.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.messages_frame.yview)
        
        # Create an Entry widget for typing messages
        self.entry_field = Entry(root, bd=5)
        self.entry_field.bind("<Return>", self.send_message)
        self.entry_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create a button to send messages
        send_button = tk.Button(root, text="Send", command=self.send_message)
        send_button.pack(side=tk.RIGHT)

    def send_message(self, event=None):
        message = self.entry_field.get()
        if message:
            self.messages_frame.insert(tk.END, "\n***********************************************************\n" + "You : " + message + "\n")
            self.messages_frame.insert(tk.END, "\n\n-------------------------------------------------------------------------\n\nmaav : " + transformer.generate_response(message)[0] + "\n\n")
            # Here, you can send the message to the other user or perform other actions.
            self.entry_field.delete(0, tk.END)  # Clear the input field

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

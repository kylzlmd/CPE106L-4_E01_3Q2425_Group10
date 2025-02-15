import tkinter as tk
from tkinter import filedialog

def select_text_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a file dialog to select a text file
    file_path = filedialog.askopenfilename(
        title="Select a text file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if file_path:
        print(f"Selected file: {file_path}")
    else:
        print("No file selected")

if __name__ == "__main__":
    select_text_file()
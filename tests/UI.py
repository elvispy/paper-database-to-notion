import tkinter as tk
from tkinter import messagebox  # Import messagebox
from main import auto_fetch_workflow, refresh_bib_thread

def call_function():
    query = entry1.get()
    project = entry2.get()
    messagebox.showinfo(title='Status', message=auto_fetch_workflow(query, project if project != "" else "uncategorized"))
    #print(f"Finished with autofetch")  # Replace with your function call

# refresh_bib_thread()
# Create the main window
root = tk.Tk()
root.title("Add your papers on notion and download them!")
root.geometry("400x300")
root.configure(bg="#2C2F33")  # Darker background for better contrast

# Style settings
label_font = ("Arial", 14)
entry_font = ("Arial", 14)
button_font = ("Arial", 14, "bold")
button_bg = "#7289DA"  # Discord-like blue
button_fg = "gray"  # White text for contrast
label_fg = "white"   # White label text

# Entry for the first input with a descriptive label
label1 = tk.Label(root, text="Enter paper identifier", bg="#2C2F33", fg=label_fg, font=label_font, anchor="w")
label1.pack(pady=(20, 5), padx=20, fill="x")
entry1 = tk.Entry(root, width=30, font=entry_font, relief="solid", bg="#FFFFFF", fg="#000000")
entry1.pack(pady=5)

# Entry for the second input with a descriptive label
label2 = tk.Label(root, text="Subfolder:", bg="#2C2F33", fg=label_fg, font=label_font, anchor="w")
label2.pack(pady=(15, 5), padx=20, fill="x")
entry2 = tk.Entry(root, width=30, font=entry_font, relief="solid", bg="#FFFFFF", fg="#000000")
entry2.pack(pady=5)

# Button to call the function
button = tk.Button(root, text="Search and download", command=call_function, font=button_font, bg=button_bg, fg=button_fg, relief="flat", width=15)
button.pack(pady=30)

# Run the UI loop
root.mainloop()

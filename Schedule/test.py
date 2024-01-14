import tkinter as tk

def fill_container():
    for i in range(6):
        for j in range(4):
            label_text = f"Label {i+1}-{j+1}"
            label = tk.Label(root, text=label_text, borderwidth=2, relief="solid")
            label.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")  # Added 'sticky' to stretch labels

# Create the main window
root = tk.Tk()
root.title("Grid Example")

# Set the window size to 1280x720 pixels
window_width = 1280
window_height = 720
root.geometry(f"{window_width}x{window_height}")

# Configure rows and columns to expand with window size
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
for j in range(4):
    root.grid_columnconfigure(j, weight=1)

# Call the function to fill the container with labels
fill_container()

# Start the Tkinter event loop
root.mainloop()
import tkinter as tk
from PIL import Image, ImageTk

# Create a root window
root = tk.Tk()

# Set the window title
root.title("You win!")

# Set the window size to fullscreen
root.attributes('-fullscreen', True)

# Load the image
image = Image.open("background_winning_screen.jpeg")  # Replace with your image path
# Resize the image to its original resolution
image = image.resize((1024, 1024), Image.BOX)
background_image = ImageTk.PhotoImage(image)

# Create a label widget to display the image
background_label = tk.Label(root, image=background_image)
# Center the label widget in the window
background_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Create a function to exit the window when the user presses the Esc key
def exit(event):
    root.destroy()

# Bind the Esc key to the exit function
root.bind('<Escape>', exit)

# Start the main loop
root.mainloop()

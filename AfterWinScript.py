import tkinter as tk
from PIL import Image, ImageTk
import subprocess
from gpiozero import Servo
from time import sleep

servo = Servo(18)

servo.value = 0.75

# Create a root window
root = tk.Tk()

# Set the window title
root.title("You win!")

# Set the window to fullscreen
root.attributes('-fullscreen', True)

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load the image
image = Image.open("background_winning_screen.jpeg")  # Replace with your image path
# Resize the image to fit the screen dimensions
image = image.resize((screen_width, screen_height), Image.BOX)
background_image = ImageTk.PhotoImage(image)

# Create a label widget to display the image
background_label = tk.Label(root, image=background_image)
background_label.pack(fill=tk.BOTH, expand=True)

# Create a function to exit the window when the user presses the Esc key
def exit(event):
    root.destroy()

# Bind the Esc key to the exit function
root.bind('<Escape>', exit)

# Start the main loop
root.mainloop()

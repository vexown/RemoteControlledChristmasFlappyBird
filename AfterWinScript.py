# Import tkinter module for GUI
import tkinter as tk

# Create a root window
root = tk.Tk()

# Set the window title
root.title("You win!")

# Set the window size to fullscreen
root.attributes('-fullscreen', True)

# Set the window background color to dark green
root.configure(bg='#006400')

# Create a label widget to display the text "You win!"
label = tk.Label(root, text="You win!", font=("Comic Sans MS", 100), fg="white", bg="#006400")

# Center the label widget in the window
label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Create a function to exit the window when the user presses the Esc key
def exit(event):
    root.destroy()

# Bind the Esc key to the exit function
root.bind('<Escape>', exit)

# ADD THE GPIO CONTROL HERE

# Start the main loop
root.mainloop()



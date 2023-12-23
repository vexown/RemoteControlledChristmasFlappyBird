from gpiozero import Servo
from time import sleep
import sys

# Create a servo instance on GPIO pin 18
servo = Servo(18)
servo.value = 1

user_position = float(input("Enter servo position (-1 to 1): "))

while True:
    servo.value = user_position
    sleep(0.2)

    # Check if a key has been pressed
    if sys.stdin.read(1) == "\n":
        break





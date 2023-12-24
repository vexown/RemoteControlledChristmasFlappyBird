from gpiozero import LED

led = LED(25)

while True:
    user_input = input("on or off?")

    if user_input == "on":
        led.on()
    elif user_input == "off":
        led.off()
    else:
        print("invalid input")




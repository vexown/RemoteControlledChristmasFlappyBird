import pgzrun
import random
import sys
import threading
import subprocess
import time

from bluepy.btle import UUID, Peripheral
import struct

from gpiozero import Servo

from gpiozero import LED

led = LED(25)

servo = Servo(18)

TITLE = 'Flappy Bird'
WIDTH = 1024
HEIGHT = 600

# These constants control the difficulty of the game
GAP = 160
GRAVITY = 100
FLAP_STRENGTH = 6.5
SPEED = 2

sensor_delay = 0

paused = False

accelerometer_data = [1,2,3]

bird = Actor('santa1', (75, 200))
bird.dead = False
bird.score = 0
bird.vy = 0

storage.setdefault('highscore', 0)

def connect_to_bluetooth(max_attempts=5):
    global service
    global characteristic
    global process

    device_address = '28:CD:C1:03:F0:24'
    TEMP_READ_UUID = "181a"
    CHARACTERISTIC_UUID = "00002a6e-0000-1000-8000-00805f9b34fb"

    attempts = 0
    connected = False
    while attempts < max_attempts and not connected:
        try:
            print(f"Connecting to the device... Attempt {attempts + 1}")
            # Establish connection
            peripheral = Peripheral(device_address)

            # Discover services and characteristics
            print("Discovering services and characteristics...")
            service_uuid = UUID(TEMP_READ_UUID)
            characteristic_uuid = UUID(CHARACTERISTIC_UUID)

            service = peripheral.getServiceByUUID(service_uuid)
            characteristic = service.getCharacteristics(characteristic_uuid)[0]

            connected = True
        except Exception as e:
            print(f"Connection attempt failed: {e}")
            attempts += 1
            time.sleep(2)  # Wait for a while before retrying

    if connected:
        # Bluetooth connection successful, proceed with your game or other logic
        print("Bluetooth connection successful. Starting the game or other logic here...")
        # Call your game logic or other functionalities here
    else:
        print("Failed to connect to Bluetooth after multiple attempts.")
        sys.exit(1)


def reset_pipes():
    pipe_gap_y = random.randint(200, HEIGHT - 200)
    pipe_top.pos = (WIDTH, pipe_gap_y - GAP // 2)
    pipe_bottom.pos = (WIDTH, pipe_gap_y + GAP // 2)


pipe_top = Actor('top', anchor=('left', 'bottom'))
pipe_bottom = Actor('bottom', anchor=('left', 'top'))
reset_pipes()  # Set initial pipe positions.


def update_pipes():
    pipe_top.left -= SPEED
    pipe_bottom.left -= SPEED
    if pipe_top.right < 0:
        reset_pipes()
        if not bird.dead:
            bird.score += 1
            if bird.score > storage['highscore']:
                storage['highscore'] = bird.score

def update_bird():
    uy = bird.vy
    y_move = accelerometer_data[2] * 0.5
    x_move = accelerometer_data[1] * 5

    bird.vy += y_move # Use the y-axis value to change the vertical velocity
    bird.y += (uy + bird.vy) / 2
    bird.x += x_move # Use the x-axis value to change the horizontal position

    #print("accel data 0:")
    #print(accelerometer_data[0])
    #print("accel data 1:")
    #print(accelerometer_data[1])
    #print("accel data 2:")
    #print(accelerometer_data[2])

    if not bird.dead:
        if bird.vy < -3:
            bird.image = 'santa2'
        else:
            bird.image = 'santa1'

    if bird.colliderect(pipe_top) or bird.colliderect(pipe_bottom):
        bird.dead = True
        bird.image = 'santa_dead'
        bird.vy = 10

    if not 0 < bird.y < 600:
        bird.y = 200
        bird.x = 200
        bird.dead = False
        bird.score = 0
        bird.vy = 0
        reset_pipes()


def update():
    global paused
    global sensor_delay
    if not paused:
        sensor_delay += 1
        
        if bird.score == 1:
            sys.exit(7)
        else:
            # Create two threads
            t2 = threading.Thread(target=update_pipes)
            t3 = threading.Thread(target=update_bird)

            # Start the threads
            if(sensor_delay == 10):
                t1 = threading.Thread(target=get_accel_data)
                t1.start()
                sensor_delay = 0
                #print("get val: ", accelerometer_data[0])
            t2.start()
            t3.start()
            #update_pipes()
            #update_bird()
            # Wait for the threads to finish
            t2.join()
            t3.join()

def on_key_down(key):
    global paused
    if key == keys.P:
        paused = not paused


def draw():
    screen.blit('background', (0, 0))
    pipe_top.draw()
    pipe_bottom.draw()
    bird.draw()
    screen.draw.text(
        str(bird.score),
        color='white',
        midtop=(WIDTH // 2, 10),
        fontsize=70,
        shadow=(1, 1)
    )
    screen.draw.text(
        "Best: {}".format(storage['highscore']),
        color=(200, 170, 0),
        midbottom=(WIDTH // 2, HEIGHT - 10),
        fontsize=30,
        shadow=(1, 1)
    )
    if paused:
        screen.draw.text(
            "PAUSED",
            color=(200, 170, 0),
            midbottom=(WIDTH // 2, HEIGHT // 2),
            fontsize=70,
            shadow=(1, 1)
        )


def get_accel_data():
    global accelerometer_data
    # Read the characteristic value
    data = characteristic.read()
    # Unpack the data into a tuple of floats
    MPU6050_array = struct.unpack('<' + 'f' * (len(data) // 4), data)
    # Get the first three values as the accelerometer data
    accelerometer_data = MPU6050_array[:3]

led.on()

servo.value = 1

# Connect to the device
connect_to_bluetooth()

#pgzrun.go()




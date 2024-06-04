from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

#get firmware from: https://github.com/pybricks/pybricks-micropython/releases/tag/v3.2.3

# Standard MicroPython modules
from usys import stdin, stdout
from uselect import poll

# Initialize the hub.
hub = PrimeHub()
"""
# Turn the light on and off 5 times.
for i in range(2):

    hub.light.on(Color(h=30, s=100, v=100))
    wait(500)

    hub.light.off()
    wait(500)

wait(1000)


# Go through all the colors.
for hue in range(360):
    hub.light.on(Color(hue))
    wait(10)
"""

hub.light.on(Color(h=30, s=100, v=100))

motor = Motor(Port.A)

# Optional: Register stdin for polling. This allows
# you to wait for incoming data without blocking.
keyboard = poll()
keyboard.register(stdin)

while True:

    # Optional: Check available input.
    while not keyboard.poll(0):
        # Optional: Do something here.
        pressed = hub.buttons.pressed()

        if Button.LEFT in pressed:
            # Send instruction to play video
            stdout.buffer.write(b"Play Video")

            # Go through all the colors.
            for hue in range(360):
                hub.light.on(Color(hue))
                wait(10)

        wait(10)

    # Read three bytes.
    cmd = stdin.buffer.read(3)

    # Decide what to do based on the command.
    if cmd == b"fwd":
        motor.dc(50)
    elif cmd == b"rev":
        motor.dc(-50)
    #elif cmd == b"bye":
        #break
    else:
        motor.stop()
    
    # Send a response.
    stdout.buffer.write(b"OK")
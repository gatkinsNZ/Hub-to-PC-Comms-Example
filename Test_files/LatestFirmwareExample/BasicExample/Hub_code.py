from pybricks.hubs import InventorHub
from pybricks.hubs import PrimeHub
from pybricks.parameters import Color
from pybricks.tools import wait

#hub = InventorHub()
hub = PrimeHub()

# Standard MicroPython modules
from usys import stdin, stdout
from uselect import poll

hub.display.char("A")
wait(1000)
hub.display.char("B")
keyboard = poll()
keyboard.register(stdin)

while True:
    stdout.buffer.write(b"r")
    
    while not keyboard.poll(0):
    # Optional: Do something here.
        wait(10)

    # Read one byte.
    cmd = stdin.buffer.read(1)
    if cmd == b"a":
        hub.light.on(Color.GREEN)
    elif cmd == b"b":
        hub.light.on(Color.RED)
    else:
        hub.light.off()
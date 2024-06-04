import asyncio
from bleak import BleakScanner, BleakClient
from pybricksdev.ble import PYBRICKS_SERVICE_UUID
from pybricksdev.ble.pybricks import Command, PYBRICKS_COMMAND_EVENT_UUID

PYBRICKS_COMMAND_EVENT_CHAR_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef"

def handle_rx(_, data: bytearray):
    if data[0] == 0x01:  # "write stdout" event (0x01)
        payload = data[1:]

        if payload == b"rdy":
            ready_event.set()
        else:
            print("Received:", payload)
            
async def main():
    legohub = await BleakScanner.find_device_by_name("Little Dawg")
    client = BleakClient(legohub)
    #print("connecting...")
    con = await client.connect()

    await client.start_notify(PYBRICKS_COMMAND_EVENT_CHAR_UUID, handle_rx)

    #print("connected")

    # Tell user to start program on the hub.
    #print("Start the program on the hub now with the button.")
    await asyncio.sleep(2)
    #print("Continue.")

    # This works
    msg = bytearray([Command.START_USER_PROGRAM])
    res = await client.write_gatt_char(PYBRICKS_COMMAND_EVENT_UUID, msg, True)
    #await asyncio.sleep(5)
    #print("Continue2")
    #msg = b'\x06a'
    #res = await client.write_gatt_char(PYBRICKS_COMMAND_EVENT_UUID, msg, True)
    #await asyncio.sleep(5)
    print("Finished1")


    await client.write_gatt_char(PYBRICKS_COMMAND_EVENT_CHAR_UUID, b'\x06a', response=True)
    await asyncio.sleep(5)
    await client.write_gatt_char(PYBRICKS_COMMAND_EVENT_CHAR_UUID, b'\x06b', response=True)
    print("Finished2")

    #await client.start_notify(PYBRICKS_COMMAND_EVENT_CHAR_UUID, handle)

    # This doesn't work (Nothing happens when the code runs. 
    # The light should turn green
    # note it does work from pybricks code interface through clicking on the terminal and typing input
    #msg = b'\x06b' # prepend the command to write to stdin
    #res = await client.write_gatt_char(PYBRICKS_COMMAND_EVENT_UUID, msg, True)
    #stdout.buffer.write(b"r")

# Run the main async program.
asyncio.run(main())
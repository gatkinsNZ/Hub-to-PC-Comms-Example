print("Program Start")


import asyncio
from bleak import BleakScanner, BleakClient

UART_SERVICE_UUID = "c5f50001-8280-46da-89f4-6d8051e4aeef"
UART_RX_CHAR_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef"
UART_TX_CHAR_UUID = "c5f50003-8280-46da-89f4-6d8051e4aeef"

#"c5f50002-8280-46da-89f4-6d8051e4aeef"

# Replace this with the name of your hub if you changed
# it when installing the Pybricks firmware.
HUB_NAME = "Little Dawg"


def hub_filter(device, ad):
    print(device.name)
    return device.name and device.name.lower() == HUB_NAME.lower()


def handle_disconnect(_):
    print("Hub was disconnected.")


def handle_rx(_, data: bytearray):
    print("Received:", data)


async def main():
    # Find the device and initialize client.
    device = await BleakScanner.find_device_by_filter(hub_filter)
    client = BleakClient(device, disconnected_callback=handle_disconnect)

    # Shorthand for sending some data to the hub.
    async def send(client, data):
        await client.write_gatt_char(rx_char, data)

    try:
        # Connect and get services.
        await client.connect()
        await client.start_notify(UART_RX_CHAR_UUID, handle_rx)
        #nus = client.services.get_service(UART_SERVICE_UUID)
        #rx_char = nus.get_characteristic(UART_RX_CHAR_UUID)
        rx_char = UART_RX_CHAR_UUID

        # Tell user to start program on the hub.
        print("Start the program on the hub now with the button.")

        # Send a few messages to the hub.
        for i in range(5):
            print("fwd")
            await send(client, b"\x06fwd")
            await asyncio.sleep(1)
            print("rev")
            await send(client, b"\x06rev")
            await asyncio.sleep(1)

        # Send a message to indicate stop.
        await send(client, b"\x06bye")

    except Exception as e:
        # Handle exceptions.
        print(e)
    finally:
        # Disconnect when we are done.
        await client.disconnect()


print("Running....")

# Run the main async program.
asyncio.run(main())

msg = "Roll a dice"
print(msg)
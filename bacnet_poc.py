import BAC0
import json
import asyncio

# Configuration
BACNET_IP = "192.168.0.100:61892"
LOCAL_IP = "192.168.0.100/24"
PORT = 47809
ANALOG_IDS = [20]  # List of analog input IDs
DIGITAL_IDS = [10]  # List of digital input IDs
READ_INTERVAL = 5  # Time interval in seconds for reading inputs

async def read_bacnet_input(bacnet, device_ip, object_type, obj_id):
    """Read a BACnet input and return the value or an error message."""
    try:
        # Use bacnet.read directly in the async function
        value = bacnet.read(f"{device_ip} {object_type} {obj_id} presentValue")
        return str(value)
    except Exception as e:
        return f"Error: {e}"

async def main():
    try:
        # Establish BACnet connection
        bacnet = BAC0.lite(ip=LOCAL_IP, port=PORT)
        
        while True:
            data = {}

            # Read analog inputs
            for analog_id in ANALOG_IDS:
                value = await read_bacnet_input(bacnet, BACNET_IP, "analogInput", analog_id)
                data[f"Analog_input_{analog_id}"] = value

            # Read digital inputs
            for digital_id in DIGITAL_IDS:
                value = await read_bacnet_input(bacnet, BACNET_IP, "binaryInput", digital_id)
                data[f"Digital_input_{digital_id}"] = value

            # Print the collected data
            print(json.dumps(data, indent=2))

            await asyncio.sleep(READ_INTERVAL)

    except Exception as e:
        print(f"Error establishing BACnet connection: {e}")
    finally:
        if 'bacnet' in locals():
            bacnet.disconnect()

if __name__ == '__main__':
    asyncio.run(main())

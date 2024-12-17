import bacpypes.app
import bacpypes.object
import bacpypes.primitivedata
import bacpypes.task

class DeviceRegistrationApp(bacpypes.app.BIPSimpleApplication):
    def __init__(self, device_address, device_id, local_address):
        """
        Initialize the BACnet device registration application
        
        :param device_address: IP address of the foreign device
        :param device_id: Device instance number
        :param local_address: Local network address
        """
        # Create a device object
        self.device_object = bacpypes.object.DeviceObject(
            objectIdentifier=('device', device_id),
            objectName=f'Foreign Device {device_id}'
        )
        
        # Initialize the application
        super().__init__(
            local_address, 
            object_list=[self.device_object]
        )
        
        # Store device parameters
        self.foreign_device_address = device_address

    def register_foreign_device(self):
        """
        Register the foreign device on the network
        """
        try:
            # Attempt to register the foreign device
            self.register_foreign_device_with_bbmd(
                self.foreign_device_address, 
                47808  # Standard BACnet UDP port
            )
            print(f"Successfully registered foreign device at {self.foreign_device_address}")
        except Exception as e:
            print(f"Device registration failed: {e}")

    def read_all_present_values(self):
        """
        Read present values from all device objects
        
        :return: Dictionary of object identifiers and their present values
        """
        present_values = {}
        
        try:
            # Discover all objects in the foreign device
            objects = self.who_is(
                low_limit=None, 
                high_limit=None, 
                device_address=self.foreign_device_address
            )
            
            # Read present value for each object
            for obj in objects:
                try:
                    value = self.read_property(
                        obj.address, 
                        obj.objectIdentifier, 
                        'presentValue'
                    )
                    present_values[obj.objectIdentifier] = value
                except Exception as read_error:
                    print(f"Could not read value for {obj.objectIdentifier}: {read_error}")
        
        except Exception as discovery_error:
            print(f"Object discovery failed: {discovery_error}")
        
        return present_values

def main():
    # Example usage
    local_address = '192.168.1.100'  # Your local IP
    foreign_device_address = '192.168.1.200'  # Foreign device IP
    device_id = 1234  # Unique device instance number

    # Create device registration application
    app = DeviceRegistrationApp(
        foreign_device_address, 
        device_id, 
        local_address
    )

    # Register the foreign device
    app.register_foreign_device()

    # Retrieve all present values
    device_values = app.read_all_present_values()
    
    # Print retrieved values
    for obj_id, value in device_values.items():
        print(f"Object {obj_id}: Present Value = {value}")

if __name__ == '__main__':
    main()
from actuator import Actuator
from leg import Leg
from point import Point3D
from pyax12.connection import Connection
import time

# Connect to the serial port
serial_connection = Connection(port="/dev/serial0", baudrate=57600)

dynamixel_id = 1

serial_connection.goto(dynamixel_id, 0, speed=512, degrees=True)
time.sleep(1)    # Wait 1 second

leg = Leg(serial_connection)

leg.move_to(Point3D(-180, 50, -60))

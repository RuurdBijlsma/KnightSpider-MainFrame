from actuator import Actuator
from leg import Leg
from point import Point3D
from pyax12.connection import Connection
import time

# Connect to the serial port
serial_connection = Connection(port="/dev/serial0", baudrate=1000000)

# allow the connection to initialize
time.sleep(1)

leg = Leg(serial_connection)

leg.move_to(Point3D(-90, 30, -70))

serial_connection.close()
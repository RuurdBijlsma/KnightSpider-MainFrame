from actuator import Actuator
from leg import Leg
from point import Point3D
from pyax12.connection import Connection
import time
import sys

# Connect to the serial port
serial_connection = Connection(port="/dev/serial0", baudrate=1000000)

# allow the connection to initialize
time.sleep(1)

leg = Leg(serial_connection)

x = 280
y = 0
z = 0
# leg.move_to(Point3D(x,y,z))

leg.shutdown()
time.sleep(2)
leg.engage()
time.sleep(2)
leg.shutdown()

print(leg.gamma.get_readings())

serial_connection.close()
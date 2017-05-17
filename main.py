from leg import Leg
from point import Point3D
from pyax12.connection import Connection
import time
import sys

try:
    import RPi.GPIO as GPIO
except:
    pass

# Connect to the serial port
GPIO.setwarnings(False)
serial_connection = Connection(port="/dev/serial0", baudrate=1000000, rpi_gpio=True, waiting_time=0.02, timeout=0.1)

# allow the connection to initialize
time.sleep(1)

leg = Leg(serial_connection)

# x = 280
# y = 0
# z = 0
# leg.move_to(Point3D(x,y,z))

# for _ in range(0, 10):
#     leg.beta.rotate_to(-70)
#     time.sleep(1)
#     leg.beta.rotate_to(70)
#     time.sleep(1)


move_delay = 1.5
leg.shutdown()
time.sleep(move_delay)
leg.engage()
time.sleep(move_delay)
leg.shutdown()

print(leg.gamma.get_readings())

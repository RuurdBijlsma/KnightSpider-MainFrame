# from pyax12.connection import Connection
import math
from time import sleep

import ax12_serial
from readings_worker import ReadingsWorker

# from spider import Spider
#
# try:
#     import RPi.GPIO as GPIO
# except:
#     pass
#
# # Connect to the serial port
# GPIO.setwarnings(False)
# serial_connection = Connection(port="/dev/serial0", baudrate=1000000, rpi_gpio=True, waiting_time=0.02, timeout=0.1)
# allow the connection to initialize
# time.sleep(1)

ax12_serial.init()

from spider import Spider

spider = Spider()

# leg1.move_to_normalized(Point3D(150, -50, 0))

#
ReadingsWorker(frequency=5, spider=spider).start()
# spider.leg_mover.set_stance(sequences['idle'][0])
spider.leg_mover.ground_clearance = 100
# spider.leg_mover.slope = Point3D(0, 1, 0)

spider.rotate_body(x_angle=math.radians(0), z_angle=math.radians(0))
#                   x vergroten is voorkant verhogen
#                   z vergroten is linkerkant verhogen
spider.leg_mover.walk(rotate_angle=math.radians(0), step_height=0, step_length=0, tip_distance=120, turn_modifier=-1)

while (True):
    spider.leg_mover.walk(rotate_angle=math.radians(0), step_height=0, step_length=0, tip_distance=int(input("")),
                          turn_modifier=-1)

# time.sleep(1)

def print_leg(leg):
    for s in leg.get_readings():
        print(s)

        # print_leg(legs[0])

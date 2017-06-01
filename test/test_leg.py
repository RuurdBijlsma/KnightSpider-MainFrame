# from pyax12.connection import Connection
import math

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
spider.leg_mover.ground_clearance = 110
spider.leg_mover.walk(rotate_angle=math.radians(0), step_height=50, step_length=40, tip_distance=110)


def print_leg(leg):
    for s in leg.get_readings():
        print(s)

        # print_leg(legs[0])

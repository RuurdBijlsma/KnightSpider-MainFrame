# from pyax12.connection import Connection

import ax12_serial
from leg import Leg

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

legs = [
    Leg(leg_id=1, angle=-30),
    Leg(leg_id=2, angle=0),
    Leg(leg_id=3, angle=30),
    Leg(leg_id=4, angle=-30),
    Leg(leg_id=5, angle=0),
    Leg(leg_id=6, angle=30),
]

# angle = 60

spider = Spider(front_left_leg=legs[0],
                mid_left_leg=legs[1],
                back_left_leg=legs[2],
                front_right_leg=legs[3],
                mid_right_leg=legs[4],
                back_right_leg=legs[5])

# leg1.move_to_normalized(Point3D(150, -50, 0))

#
# spider.leg_mover.set_stance(sequences['idle'][0])
spider.leg_mover.walk(rotate_angle=0, step_height=40, step_length=40, tip_distance=180)


def print_leg(leg):
    for s in leg.get_readings():
        print(s)

        # print_leg(legs[0])

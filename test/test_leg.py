import time

# from pyax12.connection import Connection

from leg import Leg
from movement.sequences import sequences

from point import Point3D

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

legs = [
    Leg(leg_id=1, angle=30),
    Leg(leg_id=2, angle=0),
    Leg(leg_id=3, angle=-30),
    Leg(leg_id=4, angle=-30),
    Leg(leg_id=5, angle=0),
    Leg(leg_id=6, angle=30),
]

# angle = 60
#
# spider = Spider(front_left_leg=leg1,
#                 mid_left_leg=leg2,
#                 back_left_leg=leg3,
#                 front_right_leg=leg4,
#                 mid_right_leg=leg5,
#                 back_right_leg=leg6)

# leg1.move_to_normalized(Point3D(150, -50, 0))

for index in range(0, 6):
    leg1.actuator.inverse_kinematics(Point3D(150, -50, 0))

for index in range(0, 6):
    leg1.actuator.inverse_kinematics(Point3D(150, -50, 0))
#
# spider.leg_mover.execute_stance_sequence_indefinitely(sequences["walking"])

import psutil



import ax12_serial
import time

import utils
from leg import Leg
from movement.sequences import sequences
from servo import Servo
from point import Point3D
from spider import Spider

try:
    import RPi.GPIO as GPIO
except:
    pass

def print_leg(leg):
    for s in leg.get_readings():
        print(s)

ax12_serial.init(baudrate=1000000)

# ax12_serial.scan(15)

legs = [
    Leg(-30, 1),
    Leg(0, 2),
    Leg(30, 3),
    Leg(-30, 4),
    Leg(0, 5),
    Leg(30, 6)
]


spoder = Spider(front_left_leg=legs[0],
                mid_left_leg=legs[1],
                back_left_leg=legs[2],
                front_right_leg=legs[3],
                mid_right_leg=legs[4],
                back_right_leg=legs[5])

spoder.leg_mover.execute_stance_sequence_indefinitely(sequences["walking"])
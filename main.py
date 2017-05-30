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
    Leg(-30, 11, 12, 13),
    Leg(0, 21, 22, 23),
    Leg(30, 31, 32, 33),
    Leg(-30, 41, 42, 43),
    Leg(0, 51, 52, 53),
    Leg(30, 61, 62, 63)
]


spoder = Spider(front_left_leg=legs[0],
                mid_left_leg=legs[1],
                back_left_leg=legs[2],
                front_right_leg=legs[3],
                mid_right_leg=legs[4],
                back_right_leg=legs[5])

spoder.leg_mover.execute_stance_sequence_indefinitely(sequences["walking"])
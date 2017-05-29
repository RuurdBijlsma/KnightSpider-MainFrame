import ax12_serial
import time
from leg import Leg
from servo import Servo
from point import Point3D
from subprocess import check_output

try:
    import RPi.GPIO as GPIO
except:
    pass

def print_leg(leg):
    for s in leg.get_readings():
        print(s)

ax12_serial.init()

# ax12_serial.scan(4)

leg4 = Leg(30, 41, 42, 43)

leg4.move_to_normalized(Point3D(180, -10, 30))
print_leg(leg4)

# legs = [
#     Leg(30, 11, 12, 13),
#     Leg(0, 21, 22, 23),
#     Leg(-30, 31, 32, 33),
#     Leg(30, 41, 42, 43),
# ]

# legs[2].move_to_normalized(Point3D(200, -30, -20))
# time.sleep(1)
#
# print_leg(legs[2])

# leg = Leg(-30, 1,2,3)

# result = []


# start = time.time()


# Servo(1).rotate_to(-30)
# Servo(2).rotate_to(-30)
#
#
# print("move")
# leg.move_to_normalized(Point3D(140, -30, 20))
# print(leg.get_readings()[0])
#
# print(Servo(1).get_readings())
#
# print("time", time.time() - start)
#
# time.sleep(1)
#
# ax12_serial.Ax12.port.close()
#
# for leg in legs:
#     leg.move_to_normalized(Point3D(200, -40, 20))
#
# print(Servo(1).get_readings())
#
# time.sleep(1)
# for reading in legs[0].get_readings():
#     print(reading)
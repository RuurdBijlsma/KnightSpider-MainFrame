import ax12_serial
import time
from leg import Leg
from servo import Servo
from point import Point3D

try:
    import RPi.GPIO as GPIO
except:
    pass

ax12_serial.init(timeout=0.001)

# ax12_serial.scan(3)

legs = [
    Leg(30, 11, 12, 13),
    Leg(-30, 1, 3, 4)
]

s = Servo(1)
result = []

start = time.time()

for _ in range(0, 1):
    result.append(legs[1].get_readings())

for l in result:
    for r in l:
        print(r)

print("time", time.time() - start)

# Servo(1).rotate_to(30)
#
# for leg in legs:
#     leg.move_to_normalized(Point3D(200, -40, 20))
#
# print(Servo(1).get_readings())
#
# time.sleep(1)
# for reading in legs[0].get_readings():
#     print(reading)
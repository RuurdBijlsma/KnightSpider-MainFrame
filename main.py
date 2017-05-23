import ax12_serial
import time
from leg import Leg

try:
    import RPi.GPIO as GPIO
except:
    pass

ax12_serial.init()

leg = Leg(-30, 1, 3, 4)

for reading in leg.get_readings():
    print(reading)
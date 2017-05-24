import ax12_serial
import time
from servo import Servo

try:
    import RPi.GPIO as GPIO
except:
    pass

ax12_serial.init()

scan = ax12_serial.scan(1)

new_id = 53

ax12_serial.reprogram_id(scan[0], new_id)

time.sleep(1)

Servo(new_id).rotate_to(30)

time.sleep(1)
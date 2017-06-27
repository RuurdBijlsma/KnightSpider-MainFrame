import ax12_serial
import time
from servo import Servo

try:
    import RPi.GPIO as GPIO
except:
    pass

ax12_serial.init()

ax12_serial.rotate_to(53, -30)
time.sleep(1)
ax12_serial.rotate_to(53, 30)
time.sleep(1)

# scan = ax12_serial.scan(1)
#
# new_id = 52
#
# ax12_serial.reprogram_id(1, new_id)
#
# time.sleep(1)
#
# Servo(new_id).rotate_to(30)
#
# time.sleep(1)
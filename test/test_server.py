import math
import queue

import time

import ax12_serial
from leg import Leg
from readings_worker import ReadingsWorker
from socket_listener.app_communicator import AppCommunicator
from spider import Spider

ax12_serial.init()

spider = Spider()

ReadingsWorker(frequency=5, spider=spider).start()

print(spider.get_servo_angles_json())

app = AppCommunicator(spider)

spider.leg_mover.ground_clearance = 65

spider.rotate_body(x_angle=math.radians(10), z_angle=math.radians(0))
#                   x vergroten is voorkant verhogen
#                   z vergroten is linkerkant verhogen
spider.leg_mover.walk(rotate_angle=math.radians(0), step_height=0, step_length=0, tip_distance=140, turn_modifier=0)
# spider.leg_mover.walk(rotate_angle=math.radians(0), step_height=0, step_length=0, tip_distance=110, turn_modifier=0)

print("press q to terminate")
while True:
    val = input()
    if val == 'q':
        break
    elif val == 's':
        app.server.broadcast("hey")

app.close()
print("Terminated")
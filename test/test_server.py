import math

import ax12_serial
from readings_worker import ReadingsWorker
from socket_listener.app_communicator import AppCommunicator
from spider import Spider

ax12_serial.init()

spider = Spider()

ReadingsWorker(frequency=5, spider=spider).start()

app = AppCommunicator(spider)

spider.leg_mover.ground_clearance = 80

spider.rotate_body(x_angle=math.radians(0), z_angle=math.radians(0))
#                   x vergroten is voorkant verhogen
#                   z vergroten is linkerkant verhogen
spider.leg_mover.walk(rotate_angle=math.radians(0), step_height=40, step_length=110, tip_distance=170, turn_modifier=0)


print("press q to terminate")
while True:
    val = input()
    if val == 'q':
        break
    elif val == 's':
        app.server.broadcast("hey")

app.close()
print("Terminated")
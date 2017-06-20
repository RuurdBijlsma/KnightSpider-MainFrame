import math
import time

import ax12_serial
import utils
from spider import Spider

print("temp", utils.get_cpu_temp())

ax12_serial.init()
spider = Spider()
# spider.start(False)
spider.interval_at_max_speed = 0.25
spider.speed = 1023
spider.leg_mover.ground_clearance = 100
spider.rotate_body(math.radians(-30), 0)
spider.leg_mover.clap(tip_distance=100)

while True:
    print(spider.vision.find_heart())
    time.sleep(1)

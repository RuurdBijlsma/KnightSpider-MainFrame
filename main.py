import time

import ax12_serial
import utils
from spider import Spider

print("temp", utils.get_cpu_temp())

ax12_serial.init()
spider = Spider()
spider.start(False)
# spider.interval_at_max_speed = 0.2
# spider.speed = 500
# spider.leg_mover.ground_clearance = 100
# # spider.rotate_z = math.radians(30)
# spider.rotate_body(math.radians(-40), 0)
# spider.leg_mover.clap(tip_distance=100)

while True:
    time.sleep(1)

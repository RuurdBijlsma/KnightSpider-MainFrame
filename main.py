import time

import ax12_serial
import utils
from spider import Spider

print("temp", utils.get_cpu_temp())

ax12_serial.init()
spider = Spider()
spider.start(True)
# spider.interval_at_max_speed = 0.2
# spider.speed = 500
# spider.leg_mover.ground_clearance = 100
# spider.leg_mover.walk(tip_distance=100, turn_modifier=1, rotate_angle=math.radians(-90), step_height=40, step_length=40, crab=True)

# spider.leg_mover.stop()
# spider.dance_mover.execute()

# Keep awake
while True:
    # spider.fury_mode()
    # spider.egg_mode(cards.CLUB, True)
    # spider.balance()
    time.sleep(0.3)

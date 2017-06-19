import time

import ax12_serial
import utils
from gyroscoop import Gyroscoop
from spider import Spider

print("temp", utils.get_cpu_temp())
g = Gyroscoop()
print("angle", g.get_x_rotation(g.read_gyro()))

ax12_serial.init()
spider = Spider()
spider.start(True)

while True:
    time.sleep(1)
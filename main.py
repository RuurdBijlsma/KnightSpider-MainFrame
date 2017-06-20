import time

import ax12_serial
import utils
from spider import Spider

print("temp", utils.get_cpu_temp())

ax12_serial.init()
spider = Spider()
spider.start(True)

while True:
    print(spider.vision.find_heart())
    time.sleep(1)

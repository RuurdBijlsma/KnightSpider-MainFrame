import time

import ax12_serial
from spider import Spider

ax12_serial.init()
spider = Spider()
spider.start(True)
# spider.cache_controller_ik()

time.sleep(100000)

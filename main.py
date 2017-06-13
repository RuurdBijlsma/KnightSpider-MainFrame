import ax12_serial
from spider import Spider

ax12_serial.init()
spider = Spider()
spider.start(False)

while True: pass

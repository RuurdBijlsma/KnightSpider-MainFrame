#!/usr/bin/python

import threading
import time

import utils


class ReadingsWorker(threading.Thread):
    def __init__(self, frequency, spider):
        self.delay = 1 / frequency
        self.spider = spider
        threading.Thread.__init__(self)

    def run(self):
        print("Started Readings worker at {} Hz".format(1 / self.delay))
        while True:
            time.sleep(self.delay)
            self.refresh_readings()

    def refresh_readings(self):
        self.spider.cpu_temperature = utils.get_cpu_temp()
        self.spider.cpu_usage = utils.get_cpu_usage()
        # print("Usage:", self.spider.cpu_temperature)
        # print("Temp:", self.spider.cpu_usage)
        self.spider.update_readings()

#!/usr/bin/python

import threading
import time

import utils


class ReadingUpdater(threading.Thread):
    def __init__(self, frequency, spider):
        self.delay = 1 / frequency
        self.spider = spider
        threading.Thread.__init__(self)

    def run(self):
        print("Starting worker")
        while True:
            time.sleep(self.delay)
            self.refresh_readings()

    def refresh_readings(self):
        print("Updating readings")
        print("Usage:", utils.get_cpu_usage())
        print("Temp:", utils.get_cpu_temp())
        self.temperature = utils.get_cpu_temp()
        self.cpu_usage = utils.get_cpu_usage()
        self.servo_info = self.spider.get_readings()

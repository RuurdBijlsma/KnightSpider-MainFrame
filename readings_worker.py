#!/usr/bin/python

import threading
import time

import utils
from periodic_worker import PeriodicWorker


class ReadingsWorker(PeriodicWorker):
    def __init__(self, frequency, spider):
        self.spider = spider
        PeriodicWorker.__init__(self, frequency)

    def update(self):
        self.spider.cpu_temperature = utils.get_cpu_temp()
        self.spider.cpu_usage = utils.get_cpu_usage()
        self.spider.update_readings()

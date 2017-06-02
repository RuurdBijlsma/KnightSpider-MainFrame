#!/usr/bin/python

import threading
import time

import utils


class PeriodicWorker(threading.Thread):
    def __init__(self, frequency):
        self.delay = 1 / frequency
        threading.Thread.__init__(self)

    def run(self):
        print("Started {} at {} Hz".format(self.__class__.__name__, 1 / self.delay))
        while True:
            time.sleep(self.delay)
            self.update()

    def update(self):
        pass

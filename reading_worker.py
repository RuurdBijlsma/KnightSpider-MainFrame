#!/usr/bin/python

import threading
import time


class Worker(threading.Thread):
    def __init__(self, frequency):
        self.delay = 1 / frequency
        threading.Thread.__init__(self)

    def run(self):
        print("Starting worker")
        self.refresh_readings()
        print("Exiting worker")

    def refresh_readings(self):
        while True:
            time.sleep(self.delay)
            print("Updating readings")

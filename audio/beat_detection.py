# beep beep detection
import RPi.GPIO as gpio
import time

PIN = 25
MAX_BEAT_TIME = 5
MAX_BEAT_COUNT = 3

class BeatDetection(object):
    def __init__(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(PIN, gpio.IN)

    def detect_beat(self):
        t_start = time.time()

        beats = []

        is_high = False
        while len(beats) < MAX_BEAT_COUNT and time.time() < t_start + MAX_BEAT_TIME:
            state = gpio.input(PIN)

            if state and not is_high:
                beats.append(time.time())
                is_high = True

            elif not state and is_high:
                is_high = False

        if len(beats) == 0 or len(beats) == 1:
            print("no beat detected")
            return False

        return True

    def block_till_beat(self):
        while True:
            if gpio.input(PIN):
                return True


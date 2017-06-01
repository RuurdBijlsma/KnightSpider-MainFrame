import sys
from threading import Lock

import RPi.GPIO as GPIO
from lib.memes.ax12 import Ax12
from lib.pyax12.connection import Connection

module = sys.modules[__name__]
mutex = Lock()

def init(port='/dev/serial0', baudrate=1000000, timeout=0.2,
                 waiting_time=0.0002, rpi_gpio=True):
    GPIO.setwarnings(False)
    module.pyax12_connection = Connection(port, baudrate, timeout, waiting_time, rpi_gpio)
    Ax12.port = module.pyax12_connection.serial_connection
    module.memes_connection = Ax12()
    print("Initialized serial connection at {} bps".format(module.pyax12_connection.serial_connection.baudrate))

def run_with_lock(action):
    mutex.acquire()
    try:
        return action()
    except Exception as e:
        pass
        # print("Serial error: ", e)
    finally:
        mutex.release()

def read_temperature_pyax(id):
    return run_with_lock(lambda: module.pyax12_connection.get_present_temperature(id))

def read_temperature(id):
    return run_with_lock(lambda: module.memes_connection.readTemperature(id))

def read_load(id):
    return run_with_lock(lambda: module.memes_connection.readLoad(id))

def read_voltage(id):
    return run_with_lock(lambda: module.memes_connection.readVoltage(id)) / 10

# map to degrees
def read_position(id):
    return round((run_with_lock(lambda: module.memes_connection.readPosition(id)) - 512) / 3.41, 2)

# kaput
def read_speed(id):
    return run_with_lock(lambda: module.memes_connection.readSpeed(id))

def read_moving_status(id):
    return run_with_lock(lambda: module.memes_connection.readMovingStatus(id))

def rotate_to(id, angle, speed=1023, degrees=True):
    return run_with_lock(lambda: module.pyax12_connection.goto(id, angle, speed, degrees))

def scan(num_connected):
    scan = run_with_lock(lambda: module.memes_connection.learnServos(num_connected))
    print(scan)
    return scan

def reprogram_id(old_id, new_id):
    return run_with_lock(lambda: module.memes_connection.setID(old_id, new_id))
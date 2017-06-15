import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setup(8, gpio.OUT)
pin = gpio.PWM(8, 50)

pin.start(7.5)

while True:
    pin.ChangeDutyCycle(5.5)
    time.sleep(2)
    pin.ChangeDutyCycle(10)
    time.sleep(2)
import RPi.GPIO as gpio

PIN_ID = 26
PWM_HZ = 50

pin = None

CLOSE_PWM = 5.5
OPEN_PWM = 10

def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(PIN_ID, gpio.OUT)
    pin = gpio.PWM(PIN_ID, PWM_HZ)

def open_maw():
    pin.ChangeDutyCycle(OPEN_PWM)

def close_maw():
    pin.ChangeDutyCycle(CLOSE_PWM)

def close():
    pin.stop()
    gpio.cleanup()
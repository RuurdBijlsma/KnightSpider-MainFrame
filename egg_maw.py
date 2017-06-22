import RPi.GPIO as gpio

PIN_ID = 26
PWM_HZ = 50

pin = None
current_pwm = None

CLOSE_PWM = 5.5
OPEN_PWM = 10

def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(PIN_ID, gpio.OUT)
    global pin
    pin = gpio.PWM(PIN_ID, PWM_HZ)
    pin.start(OPEN_PWM)
    global current_pwm
    current_pwm = OPEN_PWM

def open_maw():
    pin.ChangeDutyCycle(OPEN_PWM)
    global current_pwm
    current_pwm = OPEN_PWM

def close_maw():
    pin.ChangeDutyCycle(CLOSE_PWM)
    global current_pwm
    current_pwm = CLOSE_PWM

def close():
    pin.stop()
    gpio.cleanup()
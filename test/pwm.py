import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)

for i in range(1, 40):
    print(i)
    try:
        gpio.setup(i, gpio.OUT)
        pin = gpio.PWM(i, 50)

        pin.start(7.5)

        pin.ChangeDutyCycle(5.5)
        time.sleep(0.5)
        pin.ChangeDutyCycle(10)
        time.sleep(0.5)
    except:
        print("faal", i)
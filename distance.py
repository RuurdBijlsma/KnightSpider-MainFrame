import RPi.GPIO as GPIO  # Import GPIO library
import time  # Import time library

GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering

TRIG = 17  # Associate pin 23 to TRIG
ECHO = 27  # Associate pin 24 to ECHO



def init():
    GPIO.setup(TRIG, GPIO.OUT)  # Set pin as GPIO out
    GPIO.setup(ECHO, GPIO.IN)  # Set pin as GPIO in

def get_distance():
    GPIO.output(TRIG, False)  # Set TRIG as LOW
    GPIO.output(TRIG, True)  # Set TRIG as HIGH
    time.sleep(0.00001)  # Delay of 0.00001 seconds
    GPIO.output(TRIG, False)  # Set TRIG as LOW

    pulse_start = time.time()
    while GPIO.input(ECHO) == 0:  # Check whether the ECHO is LOW
        pulse_start = time.time()  # Saves the last known time of LOW pulse

    pulse_end = time.time()
    while GPIO.input(ECHO) == 1:  # Check whether the ECHO is HIGH
        pulse_end = time.time()  # Saves the last known time of HIGH pulse

    pulse_duration = pulse_end - pulse_start  # Get pulse duration to a variable

    distance = pulse_duration * 17150  # Multiply pulse duration by 17150 to get distance
    distance = round(distance, 2)  # Round to two decimal points

    if 2 < int(distance) < 400:  # Check whether the distance is within range
        print("Distance:", distance - 0.5, "cm")  # Print distance with 0.5 cm calibration
        return distance-0.5
    else:
        print("Out Of Range")  # display out of range
        return float("inf")
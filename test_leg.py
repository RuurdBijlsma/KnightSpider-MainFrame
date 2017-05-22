import time
from pyax12.connection import Connection
from leg import Leg
from sequences import sequences
from spider import Spider
from point import Point3D

try:
    import RPi.GPIO as GPIO
except:
    pass

# Connect to the serial port
GPIO.setwarnings(False)
serial_connection = Connection(port="/dev/serial0", baudrate=1000000, rpi_gpio=True, waiting_time=0.02, timeout=0.1)

# allow the connection to initialize
time.sleep(1)

leg1 = Leg(serial_connection, gamma_id=1, alpha_id=3, beta_id=4, angle=-30)
leg2 = Leg(serial_connection, gamma_id=9, alpha_id=10, beta_id=11, angle=0)
leg3 = Leg(serial_connection, gamma_id=9, alpha_id=10, beta_id=11, angle=0)
leg4 = Leg(serial_connection, gamma_id=9, alpha_id=10, beta_id=11, angle=0)
leg5 = Leg(serial_connection, gamma_id=9, alpha_id=10, beta_id=11, angle=0)
leg6 = Leg(serial_connection, gamma_id=9, alpha_id=10, beta_id=11, angle=0)

angle = 60

spider = Spider(front_left_leg=leg1,
                mid_left_leg=leg2,
                back_left_leg=leg3,
                front_right_leg=leg4,
                mid_right_leg=leg5,
                back_right_leg=leg6)

# leg1.move_to_normalized(Point3D(150, -50, 0))

spider.leg_mover.execute_stance_sequence_indefinitely(sequences["walking"])

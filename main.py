import ax12_serial
import time
from servo import Servo

try:
    import RPi.GPIO as GPIO
except:
    pass

ax12_serial.init()

servo3 = Servo(None, 3)
servo3.rotate_to(40)

time.sleep(0.1)
print("pos", ax12_serial.read_position(3))

print(servo3.get_readings())

# for _ in range(0,5):
#     ax12_serial.rotate_to(3, 60)
#     time.sleep(0.5)
#     ax12_serial.rotate_to(3, -60)
#     time.sleep(0.5)

# # Connect to the serial port
# GPIO.setwarnings(False)
# serial_connection = Connection(port="/dev/serial0", baudrate=1000000, rpi_gpio=True, waiting_time=0.04, timeout=0.1)
#
# # allow the connection to initialize
# time.sleep(1)
#
# Ax12.port = serial_connection.serial_connection
# conn = Ax12()

# print(conn.learnServos(3, 1, 254))

# leg = Leg(serial_connection, 0, 1, 3, 4)
#
# x = 200
# y = -50
# z = 100
# leg.move_to(Point3D(x,y,z))

# for _ in range(0, 10):
#     leg.beta.rotate_to(-70)
#     time.sleep(1)
#     leg.beta.rotate_to(70)a
#     time.sleep(1)

# s12 = Servo(serial_connection, 3, 0, -150, 150)
#
# move_delay = 1.5
#
# while True:
#     print("bfore read emperure")
#     print("meme temp", conn.readTemperature(3))
#     # print("READ TEMPERATURE", serial_connection.get_present_temperature(3))
#     s12.rotate_to(-60)
#     time.sleep(move_delay)
#     s12.rotate_to(60)
#     time.sleep(move_delay)
#
# # leg.move_to(Point3D(280, -1, 0))
# # time.sleep(move_delay)
# # leg.move_to(Point3D(200, -2, 0))
# # leg.shutdown()
# # time.sleep(move_delay)
# # leg.engage()
# # time.sleep(move_delay)
# # leg.shutdown()
#
# print(leg.gamma.get_readings())

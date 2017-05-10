from actuator import Actuator
from servo import Servo


class Leg(object):
    ALPHA_ID = 1
    BETA_ID = 2
    GAMMA_ID = 3

    def __init__(self, serial_connection):
        self.serial_connection = serial_connection
        self.actuator = Actuator(['z', [65, 0., 0.], 'y', [100, 0., 0.], 'y', [65, 0., 0.]])
        self.alpha = Servo(serial_connection, self.ALPHA_ID, -90, 90)
        self.beta = Servo(serial_connection, self.BETA_ID, -90, 90)
        self.gamma = Servo(serial_connection, self.GAMMA_ID, -90, 90)

    def move_to(self, point):
        angles = self.actuator.inverse_kinematics(point)

        self.gamma.rotate(angles[0])

        # Rotate using old method
        self.rotate_servo(self.GAMMA_ID, angles[0])


        self.alpha.rotate(angles[1])
        self.beta.rotate(angles[2])

    def rotate_servo(self, id, angle):
        self.serial_connection.goto(id, angle, speed=512, degrees=True)

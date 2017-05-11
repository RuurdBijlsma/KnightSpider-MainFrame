from actuator import Actuator
from servo import Servo


class Leg(object):
    ALPHA_ID = 1
    BETA_ID = 2
    GAMMA_ID = 3

    def __init__(self, serial_connection):
        self.serial_connection = serial_connection
        self.actuator = Actuator(['y', [80, 0., 0.], 'z', [80, 0., 0.], 'z', [120, 0., 0.]])
        self.alpha = Servo(serial_connection, self.ALPHA_ID, -90, 90)
        self.beta = Servo(serial_connection, self.BETA_ID, -90, 90)
        self.gamma = Servo(serial_connection, self.GAMMA_ID, -160, 10)

    def move_to(self, point):
        angles = self.actuator.inverse_kinematics(point)
        print("angles", angles)
        self.gamma.rotate(angles[0])
        self.alpha.rotate(angles[1])
        self.beta.rotate(angles[2])

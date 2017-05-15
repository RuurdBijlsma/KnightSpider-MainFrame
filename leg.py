from inverse_kinematics.actuator import Actuator
from servo import Servo


class Leg(object):
    GAMMA_ID = 1
    ALPHA_ID = 2
    BETA_ID = 3

    def __init__(self, serial_connection):
        self.serial_connection = serial_connection
        self.actuator = Actuator(['y', [80, 0., 0.], 'z', [80, 0., 0.], 'z', [120, 0., 0.]],
                                 max_angles=[150, 150, 150],
                                 min_angles=[-150, -150, -150])
        self.gamma = Servo(serial_connection, self.GAMMA_ID, -90, 90)
        self.alpha = Servo(serial_connection, self.ALPHA_ID, -150, 80, flip_angles=True)
        self.beta = Servo(serial_connection, self.BETA_ID, -120, 150)

    def move_to(self, point):
        angles = self.actuator.inverse_kinematics(point)
        print("angles", angles)
        self.gamma.rotate(angles[0])
        self.alpha.rotate(angles[1])
        self.beta.rotate(angles[2])

    def shutdown(self):
        self.gamma.rotate(0)
        self.alpha.rotate(-150)
        self.beta.rotate(150)

    def engage(self):
        self.gamma.rotate(0)
        self.alpha.rotate(0)
        self.beta.rotate(60)

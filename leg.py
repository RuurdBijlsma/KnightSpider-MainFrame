from inverse_kinematics.actuator import Actuator
from servo import Servo


class Leg(object):
    GAMMA_ID = 15
    ALPHA_ID = 6
    BETA_ID = 16

    def __init__(self, serial_connection):
        self.serial_connection = serial_connection
        self.actuator = Actuator(['y', [80, 0., 0.], 'z', [80, 0., 0.], 'z', [120, 0., 0.]],
                                 max_angles=[150, 150, 150],
                                 min_angles=[-150, -150, -150])
        self.gamma = Servo(serial_connection, self.GAMMA_ID, -60, 60)
        self.alpha = Servo(serial_connection, self.ALPHA_ID, -140, 70, flip_angles=True)
        self.beta = Servo(serial_connection, self.BETA_ID, -90, 140)

    def move_to(self, point):
        angles = self.actuator.inverse_kinematics(point)
        print("angles", angles)
        self.gamma.rotate_to(angles[0])
        self.alpha.rotate_to(angles[1])
        self.beta.rotate_to(angles[2])

    def shutdown(self):
        self.gamma.rotate_to(-30)
        self.alpha.rotate_to(-100)
        self.beta.rotate_to(100)

    def engage(self):
        self.gamma.rotate_to(30)
        self.alpha.rotate_to(70)
        self.beta.rotate_to(0)

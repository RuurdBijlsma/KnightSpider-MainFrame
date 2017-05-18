from inverse_kinematics.actuator import Actuator
from servo import Servo
from point import Point3D


class Leg(object):
    GAMMA_ID = 15
    ALPHA_ID = 6
    BETA_ID = 16

    def __init__(self, serial_connection):
        self.serial_connection = serial_connection
        self.actuator = Actuator(['y', [77, 0., 0.], 'z', [80, 0., 0.], 'z', [115, 0., 0.]],
                                 max_angles=[150, 150, 150],
                                 min_angles=[-150, -150, -150])
        self.gamma = Servo(serial_connection, self.GAMMA_ID, offset_angle=0, min_angle=-60, max_angle=60)
        self.alpha = Servo(serial_connection, self.ALPHA_ID, offset_angle=0, min_angle=-140, max_angle=70, flip_angles=True)
        self.beta = Servo(serial_connection, self.BETA_ID, offset_angle=0, min_angle=-90, max_angle=140)

    def move_to(self, point):
        assert(point.y < 0)
        angles = self.actuator.inverse_kinematics(point)
        # print("angles", point, angles)
        self.gamma.rotate_to(angles[0])
        self.alpha.rotate_to(angles[1])
        self.beta.rotate_to(angles[2])

    def shutdown(self):
        self.move_to(Point3D(130, -5, 0))

    def engage(self):
        print("am enage")
        self.move_to(Point3D(180, -70, 0))

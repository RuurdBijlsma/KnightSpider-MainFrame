import math

from inverse_kinematics.actuator import Actuator
from servo import Servo
from point import Point3D


def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


class Leg(object):
    GAMMA_ID = 15
    ALPHA_ID = 6
    BETA_ID = 16

    def __init__(self, serial_connection, angle, gamma_id, alpha_id, beta_id):
        self.serial_connection = serial_connection
        self.actuator = Actuator(['y', [77, 0., 0.], 'z', [80, 0., 0.], 'z', [115, 0., 0.]],
                                 max_angles=[150, 150, 150],
                                 min_angles=[-150, -150, -150])
        self.gamma = Servo(serial_connection, self.GAMMA_ID, offset_angle=0, min_angle=-60, max_angle=60)
        self.alpha = Servo(serial_connection, self.ALPHA_ID, offset_angle=0, min_angle=-140, max_angle=70,
                           flip_angles=True)
        self.beta = Servo(serial_connection, self.BETA_ID, offset_angle=0, min_angle=-90, max_angle=140)

        self.ground_height_offset = 0
        self.angle = angle

    def point_to_normalized(self, point):
        origin = (0, 0)
        tip_point = (point.x, point.z)
        x, z = rotate(origin, tip_point, math.radians(self.angle))
        return Point3D(x, point.y, z)

    def move_to_normalized(self, point):
        self.move_to(self.point_to_normalized(point))

    def move_to(self, point):
        point.y += self.ground_height_offset
        assert (point.y < 0)
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

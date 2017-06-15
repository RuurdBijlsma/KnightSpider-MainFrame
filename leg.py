import math

from lib.inverse_kinematics.actuator import Actuator

import ax12_serial
from point import Point3D
from servo import Servo


class Leg(object):
    def __init__(self, ik_cache, angle, leg_id, body_position):
        self.actuator = Actuator(cache=ik_cache,
                                 arm_definition=['y', [60, 0., 0.], 'z', [70, 0., 0.], 'z', [111, 0., 0.]],
                                 max_angles=[150, 150, 150],
                                 min_angles=[-150, -150, -150])
        self.gamma = Servo(leg_id * 10 + 1, offset_angle=0, min_angle=-150, max_angle=150)
        self.alpha = Servo(leg_id * 10 + 2, offset_angle=0, min_angle=-150, max_angle=150,
                           flip_angles=True)
        self.beta = Servo(leg_id * 10 + 3, offset_angle=0, min_angle=-150, max_angle=150)

        self.ground_height_offset = 0
        self.angle = angle
        self.body_position = body_position
        self.is_left_leg = body_position.x < 0

    def point_to_normalized(self, point, midpoint, crab=False):
        midpoint = (0, 0) if crab else (midpoint.x, midpoint.z)
        rotated_point = point.rotate_around_y(midpoint, math.radians(self.angle))
        return rotated_point if self.is_left_leg else rotated_point.negate_z()

    def move_to_normalized(self, point, midpoint, crab=False, on_done=lambda: None):
        return self.move_to(self.point_to_normalized(point, midpoint, crab), on_done)

    def get_tip_point(self):
        gamma_angle = self.gamma.angle
        alpha_angle = self.alpha.angle
        beta_angle = self.beta.angle
        return self.actuator.forward_kinematics([gamma_angle, alpha_angle, beta_angle])

    def get_body_to_tip_point(self):
        return self.body_position + self.get_tip_point()

    def move_to(self, point, on_done=lambda: None):
        point.y += self.ground_height_offset * (-1 if self.is_left_leg else 1)

        # point.y = -1 if point.y >= 0 else point.y

        angles = self.actuator.inverse_kinematics(point)
        # print("angles", point, angles)

        self.servos_to_do = 3

        def on_done_callback():
            self.servos_to_do -= 1
            if (self.servos_to_do == 0):
                on_done()

        ax12_serial.lock()
        try:
            self.beta.rotate_to(angles[2], on_done_callback)
            self.alpha.rotate_to(angles[1], on_done_callback)
            self.gamma.rotate_to(angles[0], on_done_callback)
        finally:
            ax12_serial.unlock()

    def shutdown(self):
        self.move_to(Point3D(130, -5, 0))

    def engage(self):
        print("am enage")
        self.move_to(Point3D(180, -70, 0))

    def update_readings(self):
        self.gamma.update_readings()
        self.alpha.update_readings()
        self.beta.update_readings()

    @property
    def readings(self):
        return [
            self.gamma.readings,
            self.alpha.readings,
            self.beta.readings
        ]

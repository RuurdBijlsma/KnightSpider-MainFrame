import math
import sched

import time

from lib.inverse_kinematics.actuator import Actuator
from point import Point3D
from promise.promise import Promise
from servo import Servo
from utils import rotate


class Leg(object):
    def __init__(self, angle, gamma_id, alpha_id, beta_id):
        self.actuator = Actuator(['y', [77, 0., 0.], 'z', [80, 0., 0.], 'z', [115, 0., 0.]],
                                 max_angles=[150, 150, 150],
                                 min_angles=[-150, -150, -150])
        self.gamma = Servo(gamma_id, offset_angle=0, min_angle=-60, max_angle=60)
        self.alpha = Servo(alpha_id, offset_angle=0, min_angle=-140, max_angle=70,
                           flip_angles=True)
        self.beta = Servo(beta_id, offset_angle=0, min_angle=-90, max_angle=140)

        self.ground_height_offset = 0
        self.angle = angle

    def point_to_normalized(self, point):
        origin = (0, 0)
        tip_point = (point.x, point.z)
        x, z = rotate(origin, tip_point, math.radians(self.angle))
        return Point3D(x, point.y, z)

    def move_to_normalized(self, point):
        return self.move_to(self.point_to_normalized(point))

    def get_servo_positions(self):
        # gamma_angle = self.gamma.info.angle
        # alpha_angle = self.alpha.info.angle
        # beta_angle = self.beta.info.angle
        return self.actuator.forward_kinematics([gamma_angle, alpha_angle, beta_angle])

    def check_distance(self, target_pos, distance_threshold=5):
        return self.get_servo_positions().distance_to(target_pos) < distance_threshold

    def move_to(self, point):
        # def promise(resolve):
        point.y += self.ground_height_offset
        assert (point.y < 0)
        angles = self.actuator.inverse_kinematics(point)
        # print("angles", point, angles)
        self.gamma.rotate_to(angles[0])
        self.alpha.rotate_to(angles[1])
        self.beta.rotate_to(angles[2])

            # Check if leg reached point
        #     s = sched.scheduler(time.time, time.sleep)
        #     timer_delay = 0.2
        #     first_check_delay = 0.1
        #
        #     def timer():
        #         if (self.check_distance(point)):
        #             resolve()
        #
        #         s.enter(timer_delay, 1, timer)
        #
        #     s.enter(first_check_delay, 1, timer)
        #     s.run()
        #
        # return Promise(promise)

    def shutdown(self):
        self.move_to(Point3D(130, -5, 0))

    def engage(self):
        print("am enage")
        self.move_to(Point3D(180, -70, 0))

    def get_readings(self):
        return [
            self.gamma.get_readings(),
            self.alpha.get_readings(),
            self.beta.get_readings()
        ]

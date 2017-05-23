import sched
import time

from point import Point3D
from promise.promise import Promise


class LegMover(object):
    def __init__(self, spider, ground_clearance):
        self.spider = spider
        self.ground_clearance = ground_clearance
        self.cancel = False

    def get_leg_position(self, leg):
        gamma_angle = leg.gamma.info.angle
        alpha_angle = leg.alpha.info.angle
        beta_angle = leg.beta.info.angle
        return leg.actuator.forward_kinematics([gamma_angle, alpha_angle, beta_angle])

    def check_leg(self, leg, target_pos, distance_threshold=5):
        return self.get_leg_position(leg).distance_to(target_pos) < distance_threshold

    def set_stance(self, stance):
        def promise(resolve):
            legs = []
            for xp, dict in stance.points.items():
                for yp, point in dict.items():
                    leg = self.spider.legs[xp][yp]
                    legs.append(leg)
                    point = Point3D(point.x, point.y - self.ground_clearance, point.z)
                    leg.move_to_normalized(point)

            # Check if leg reached point
            s = sched.scheduler(time.time, time.sleep)
            timer_delay = 0.2

            legs_to_do = len(legs)

            def timer():
                global legs_to_do
                for xp, dict in stance.points.items():
                    for yp, point in dict.items():
                        leg = self.spider.legs[xp][yp]
                        point = Point3D(point.x, point.y - self.ground_clearance, point.z)
                        if (self.check_leg(leg, point)):
                            legs_to_do = legs_to_do - 1
                        if (legs_to_do == 0):
                            resolve()

                s.enter(timer_delay, 1, timer)

            s.enter(timer_delay, 1, timer)
            s.run()

        return Promise(promise)

    def execute_stance_sequence_indefinitely(self, stance_list, index=None):
        if (index == None or index == -1):
            index = len(stance_list) - 1

        if (not self.cancel):
            self.set_stance(stance_list[index]).then(
                lambda: self.execute_stance_sequence_indefinitely(stance_list, index - 1)
            )
        else:
            self.cancel = False

    def execute_stance_sequence(self, stance_list):
        stance, *remaining_stances = stance_list

        if (not self.cancel):
            self.set_stance(stance).then(lambda: self.execute_stance_sequence(remaining_stances))
        else:
            self.cancel = False


def cancel_sequence(self):
    self.cancel = True

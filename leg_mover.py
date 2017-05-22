import time

from point import Point3D


class LegMover(object):
    def __init__(self, spider, ground_clearance):
        self.spider = spider
        self.ground_clearance = ground_clearance
        self.cancel = False

    def set_stance(self, stance):
        for xp, dict in stance.points.items():
            for yp, point in dict.items():
                leg = self.spider.legs[xp][yp]
                point = Point3D(point.x, point.y - self.ground_clearance, point.z)
                leg.move_to_normalized(point)

    def execute_stance_sequence_indefinitely(self, stance_delay_tuples):
        while (True):
            if (self.cancel):
                break
            self.execute_stance_sequence(stance_delay_tuples)

    def execute_stance_sequence(self, stance_delay_tuples):
        for stance, delay in stance_delay_tuples:
            if (self.cancel):
                break

            self.set_stance(stance)
            time.sleep(delay)

    def cancel_sequence(self):
        self.cancel = True

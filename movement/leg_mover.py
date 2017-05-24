from point import Point3D


class LegMover(object):
    def __init__(self, spider, ground_clearance):
        self.spider = spider
        self.ground_clearance = ground_clearance
        self.cancel = False

    def set_stance(self, stance, on_done):
        self.legs_to_do = 0

        for xp, dict in stance.points.items():
            for yp, point in dict.items():
                leg = self.spider.legs[xp][yp]
                point = Point3D(point.x, point.y - self.ground_clearance, point.z)

                self.legs_to_do = self.legs_to_do + 1

                def on_done_callback():
                    self.legs_to_do = self.legs_to_do - 1
                    if (self.legs_to_do == 0):
                        on_done()

                leg.move_to_normalized(point, on_done_callback)

    def execute_stance_sequence_indefinitely(self, stance_list, index=None):
        if (index == None or index == -1):
            index = len(stance_list) - 1

        if (not self.cancel):
            self.set_stance(stance_list[index],
                            lambda: self.execute_stance_sequence_indefinitely(stance_list, index - 1))
        else:
            self.cancel = False

    def execute_stance_sequence(self, stance_list):
        stance, *remaining_stances = stance_list

        if (not self.cancel):
            self.set_stance(stance, lambda: self.execute_stance_sequence(remaining_stances))
        else:
            self.cancel = False


def cancel_sequence(self):
    self.cancel = True

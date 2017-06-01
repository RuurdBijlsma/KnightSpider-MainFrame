import math

from movement.stance import Stance

from point import Point3D


class LegMover(object):
    def __init__(self, spider, ground_clearance):
        self.spider = spider
        self.ground_clearance = ground_clearance
        self.cancel = False
        self.current_walk_index = None
        self.is_moving = False

    def walk(self, rotate_angle=math.radians(0), step_length=40, step_height=40, tip_distance=180, rotate=False):
        forward = 0
        back = 1
        lifted = 2

        rotate_origin = (tip_distance, 0)

        points = [
            Point3D(tip_distance, 0, step_length / 2),
            Point3D(tip_distance, 0, -step_length / 2),
            Point3D(tip_distance, step_height, 0)
        ]

        points_right = [point.rotate_around_y(rotate_origin, rotate_angle) for point in points]
        points_left = points

        if (rotate):
            points_left = [point.negate_z() for point in points_left]

        points_left = [point.rotate_around_y(rotate_origin, rotate_angle) for point in points_left]

        stance_sequence = [
            Stance(
                front_left_point=points_left[forward],
                mid_left_point=points_left[back],
                back_left_point=points_left[forward],
                front_right_point=points_right[back],
                mid_right_point=points_right[forward],
                back_right_point=points_right[back]
            ),
            Stance(
                front_left_point=points_left[back],
                mid_left_point=points_left[lifted],
                back_left_point=points_left[back],
                front_right_point=points_right[lifted],
                mid_right_point=points_right[back],
                back_right_point=points_right[lifted]
            ),
            Stance(
                front_left_point=points_left[back],
                mid_left_point=points_left[forward],
                back_left_point=points_left[back],
                front_right_point=points_right[forward],
                mid_right_point=points_right[back],
                back_right_point=points_right[forward]
            ),
            Stance(
                front_left_point=points_left[lifted],
                mid_left_point=points_left[back],
                back_left_point=points_left[lifted],
                front_right_point=points_right[back],
                mid_right_point=points_right[lifted],
                back_right_point=points_right[back]
            ),
        ]

        if self.is_moving:
            self.cancel_sequence()
        self.execute_stance_sequence_indefinitely(stance_sequence, self.current_walk_index)

    def set_stance(self, stance, on_done=lambda: None):
        self.legs_to_do = 0

        for xp, dict in stance.points.items():
            for yp, point in dict.items():
                leg = self.spider.legs[xp][yp]
                point = Point3D(point.x, point.y - self.ground_clearance, point.z)

                self.legs_to_do = self.legs_to_do + 1

                def on_done_callback():
                    self.legs_to_do = self.legs_to_do - 1
                    if self.legs_to_do == 0:
                        on_done()

                leg.move_to_normalized(point, on_done_callback)

    def execute_stance_sequence_indefinitely(self, stance_list, index=None):
        if index == None or index == -1:
            index = len(stance_list) - 1

        self.current_walk_index = index

        if not self.cancel:
            self.is_moving = True
            self.set_stance(stance_list[index],
                            lambda: self.execute_stance_sequence_indefinitely(stance_list, index - 1))
        else:
            self.cancel = False

    def execute_stance_sequence(self, stance_list):
        stance, *remaining_stances = stance_list

        if not self.cancel:
            self.is_moving = True
            self.set_stance(stance, lambda: self.execute_stance_sequence(remaining_stances))
        else:
            self.cancel = False

    def cancel_sequence(self):
        self.cancel = True
        self.is_moving = False

import math

import utils
from movement.stance import Stance
from point import Point3D


class LegMover(object):
    def __init__(self, spider, ground_clearance=50):
        self.spider = spider
        self.ground_clearance = ground_clearance
        self.cancel = False
        self.current_walk_index = None
        self.is_moving = False

    def walk(self, rotate_angle=math.radians(0), step_length=80, step_height=40, tip_distance=180, turn_modifier=0):
        # Turning modifier 1 betekent naar rechts draaien om zijn as
        # Turning modifier -1 betekent naar links draaien om zijn as
        # Turning modifier 0.5 betekent naar rechts sturen terwijl hij loopt
        forward = 0
        back = 1
        lifted = 2

        left_legs_speed_multiplier = 1
        right_legs_speed_multiplier = 1
        if (turn_modifier > 0):
            left_legs_speed_multiplier = 1 - turn_modifier * 2
        else:
            right_legs_speed_multiplier = 1 + turn_modifier * 2

        rotate_origin = (tip_distance, 0)

        points = [
            Point3D(tip_distance, 0, step_length / 2),  # forward
            Point3D(tip_distance, 0, -step_length / 2),  # back
            Point3D(tip_distance, step_height, 0)  # lifted
        ]

        points_left = points
        points_right = points

        if (right_legs_speed_multiplier != 1):
            points_right = [point.multiply_z(right_legs_speed_multiplier) for point in points_left]

        if (left_legs_speed_multiplier != 1):
            points_left = [point.multiply_z(left_legs_speed_multiplier) for point in points_left]

        points_right = [point.rotate_around_y(rotate_origin, rotate_angle) for point in points_right]
        points_left = [point.rotate_around_y(rotate_origin, rotate_angle) for point in points_left]

        midpoints = {
            'right': utils.midpoint(points_right[back], points_right[forward]),
            'left': utils.midpoint(points_left[back], points_left[forward])
        }

        stance_sequence = [
            Stance(
                front_left_point=points_left[forward],
                mid_left_point=points_left[back],
                back_left_point=points_left[forward],
                front_right_point=points_right[back],
                mid_right_point=points_right[forward],
                back_right_point=points_right[back],
                midpoints=midpoints
            ),
            Stance(
                front_left_point=points_left[back],
                mid_left_point=points_left[lifted],
                back_left_point=points_left[back],
                front_right_point=points_right[lifted],
                mid_right_point=points_right[back],
                back_right_point=points_right[lifted],
                midpoints=midpoints
            ),
            Stance(
                front_left_point=points_left[back],
                mid_left_point=points_left[forward],
                back_left_point=points_left[back],
                front_right_point=points_right[forward],
                mid_right_point=points_right[back],
                back_right_point=points_right[forward],
                midpoints=midpoints
            ),
            Stance(
                front_left_point=points_left[lifted],
                mid_left_point=points_left[back],
                back_left_point=points_left[lifted],
                front_right_point=points_right[back],
                mid_right_point=points_right[lifted],
                back_right_point=points_right[back],
                midpoints=midpoints
            )
        ]

        if self.is_moving:
            self.cancel_sequence(
                lambda: self.execute_stance_sequence_indefinitely(stance_sequence, self.current_walk_index)
            )
        else:
            self.execute_stance_sequence_indefinitely(stance_sequence, self.current_walk_index)

    def set_stance(self, stance, on_done=lambda: None):
        self.legs_to_do = 0

        for xp, dict in stance.points.items():
            for yp, point in dict.items():
                leg = self.spider.legs[xp][yp]
                point = Point3D(point.x, point.y - self.ground_clearance, point.z)

                if (point.y >= 0):
                    print("[ERROR] Y value (%s) >= 0, setting y to -1" % point.y)
                    point.y = -1

                self.legs_to_do = self.legs_to_do + 1
                midpoint = stance.midpoints[xp]

                def on_done_callback():
                    self.legs_to_do = self.legs_to_do - 1
                    if self.legs_to_do == 0:
                        on_done()

                leg.move_to_normalized(point, midpoint, on_done_callback)

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
            self.on_cancel_listener()

    def execute_stance_sequence(self, stance_list):
        stance, *remaining_stances = stance_list

        if not self.cancel:
            self.is_moving = True
            self.set_stance(stance, lambda: self.execute_stance_sequence(remaining_stances))
        else:
            self.cancel = False
            self.on_cancel_listener()

    def cancel_sequence(self, on_cancelled=lambda: None):
        self.on_cancel_listener = on_cancelled
        self.cancel = True
        self.is_moving = False

import math

from movement.stance import Stance

import utils
from point import Point3D


class LegMover(object):
    def __init__(self, spider, ground_clearance):
        self.spider = spider
        self.ground_clearance = ground_clearance
        self.cancel = False
        self.current_walk_index = None
        self.is_moving = False

    def walk(self, rotate_angle=math.radians(0), step_length=40, step_height=40, tip_distance=180):
        forward_point_right = Point3D(tip_distance, 0, step_length / 2)
        back_point_right = Point3D(tip_distance, 0, -step_length / 2)
        lifted_point_right = Point3D(tip_distance, step_height, 0)

        forward_point_left = forward_point_right.negate_z()
        back_point_left = back_point_right.negate_z()
        lifted_point_left = lifted_point_right.negate_z()

        rotate_origin = (tip_distance, 0)
        forward_x, forward_z = utils.rotate(rotate_origin, (forward_point_right.x, forward_point_right.z), rotate_angle)
        back_x, back_z = utils.rotate(rotate_origin, (back_point_right.x, back_point_right.z), rotate_angle)
        lifted_x, lifted_z = utils.rotate(rotate_origin, (lifted_point_right.x, lifted_point_right.z), rotate_angle)

        forward_point_right.x = forward_x
        forward_point_right.z = forward_z
        back_point_right.x = back_x
        back_point_right.z = back_z
        lifted_point_right.x = lifted_x
        lifted_point_right.z = lifted_z

        rotate_origin = (tip_distance, 0)
        forward_x, forward_z = utils.rotate(rotate_origin, (forward_point_left.x, forward_point_left.z), rotate_angle)
        back_x, back_z = utils.rotate(rotate_origin, (back_point_left.x, back_point_left.z), rotate_angle)
        lifted_x, lifted_z = utils.rotate(rotate_origin, (lifted_point_left.x, lifted_point_left.z), rotate_angle)

        forward_point_left.x = forward_x
        forward_point_left.z = forward_z
        back_point_left.x = back_x
        back_point_left.z = back_z
        lifted_point_left.x = lifted_x
        lifted_point_left.z = lifted_z

        stance_sequence = [
            Stance(
                front_left_point=forward_point_left,
                mid_left_point=back_point_left,
                back_left_point=forward_point_left,
                front_right_point=back_point_right,
                mid_right_point=forward_point_right,
                back_right_point=back_point_right
            ),
            Stance(
                front_left_point=back_point_left,
                mid_left_point=lifted_point_left,
                back_left_point=back_point_left,
                front_right_point=lifted_point_right,
                mid_right_point=back_point_right,
                back_right_point=lifted_point_right
            ),
            Stance(
                front_left_point=back_point_left,
                mid_left_point=forward_point_left,
                back_left_point=back_point_left,
                front_right_point=forward_point_right,
                mid_right_point=back_point_right,
                back_right_point=forward_point_right
            ),
            Stance(
                front_left_point=lifted_point_left,
                mid_left_point=back_point_left,
                back_left_point=lifted_point_left,
                front_right_point=back_point_right,
                mid_right_point=lifted_point_right,
                back_right_point=back_point_right
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

import math

import utils
from movement.stance import Stance
from point import Point3D


class LegMover(object):
    def __init__(self, spider, ground_clearance=50):
        self.spider = spider
        self.ground_clearance = ground_clearance

    def clap(self, bpm=120, tip_distance=140, mid_leg_front_pos=20, clap_size=50):
        claps_per_second = bpm / 60

        leg_pos = Point3D(tip_distance, 0, 0)
        mid_leg_pos = Point3D(tip_distance, 0, mid_leg_front_pos)

        open = 0
        closed = 1

        clap_height = 50
        clap_closed_z = -60
        clap_points = [
            Point3D(tip_distance, clap_height, clap_closed_z + clap_size),  # open clap
            Point3D(tip_distance, clap_height, clap_closed_z)  # closed clap
        ]

        midpoints = {
            'right': utils.midpoint(clap_points[open], clap_points[open]),
            'left': utils.midpoint(clap_points[open], clap_points[open])
        }

        stance_sequence = [
            Stance(
                front_left_point=clap_points[open],
                mid_left_point=mid_leg_pos,
                back_left_point=leg_pos,
                front_right_point=clap_points[open],
                mid_right_point=mid_leg_pos,
                back_right_point=leg_pos,
                midpoints=midpoints
            ),
            Stance(
                front_left_point=clap_points[closed],
                mid_left_point=mid_leg_pos,
                back_left_point=leg_pos,
                front_right_point=clap_points[closed],
                mid_right_point=mid_leg_pos,
                back_right_point=leg_pos,
                midpoints=midpoints
            ),
        ]

        if self.current_walk_index is not None:
            self.clear_interval(self.current_walk_index)
        self.current_walk_index = self.execute_stance_sequence(stance_sequence)

    def walk(self, rotate_angle=math.radians(0), step_length=0, step_height=0, tip_distance=140, turn_modifier=0,
             crab=False):
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

        if self.current_walk_index is not None:
            self.clear_interval(self.current_walk_index)
        self.current_walk_index = self.execute_stance_sequence(stance_sequence, crab=crab)

    def set_stance(self, stance, crab=False, on_done=lambda: None):
        self.legs_to_do = 0

        for xp, dict in stance.points.items():
            for yp, point in dict.items():
                leg = self.spider.legs[xp][yp]
                point = Point3D(point.x, point.y - self.ground_clearance, point.z)

                self.legs_to_do = self.legs_to_do + 1
                midpoint = stance.midpoints[xp]

                def on_done_callback():
                    self.legs_to_do = self.legs_to_do - 1
                    if self.legs_to_do == 0:
                        on_done()

                leg.move_to_normalized(point, midpoint, crab, on_done_callback)

    sequence_amount = 0
    current_walk_index = None
    cancelled_indices = []

    def execute_stance_sequence(self, stance_list, interval_index=None, index=None, crab=False):
        index = len(stance_list) - 1 if index is None or index == -1 else index

        if interval_index is None:
            self.sequence_amount += 1
            interval_index = self.sequence_amount

        self.current_walk_index = index

        if interval_index not in self.cancelled_indices:
            self.set_stance(stance_list[index], crab,
                            lambda: self.execute_stance_sequence(stance_list, interval_index, index - 1, crab))
        else:
            print("Cancelled")
            self.cancelled_indices.remove(interval_index)

        return interval_index

    def clear_interval(self, interval_id):
        if self.current_walk_index == interval_id:
            self.current_walk_index = None
        self.cancelled_indices.append(interval_id)

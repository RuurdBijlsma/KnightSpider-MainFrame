import math
import threading
from movement.stance import Stance

import ax12_serial
import utils
from point import Point3D


class LegMover(object):
    def __init__(self, spider, ground_clearance=50):
        self.spider = spider
        self.ground_clearance = ground_clearance

    def clap(self, tip_distance=140, mid_leg_front_pos=100):
        leg_pos = Point3D(tip_distance, 0, 0)
        mid_leg_pos = Point3D(tip_distance, 0, mid_leg_front_pos)

        open = 0
        closed = 1

        clap_radius = 240
        clap_height = 200
        closed_x_pos = 0
        clap_points = [
            Point3D(clap_radius, clap_height, clap_radius),  # open clap
            Point3D(closed_x_pos, clap_height, clap_radius)  # closed clap
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


        self.sequence_amount += 1
        self.current_walk_index = self.sequence_amount
        self.execute_stance_sequence(stance_sequence, interval_index=self.current_walk_index)

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
            points_right = [point.multiply_z(right_legs_speed_multiplier) for point in points_right]

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

        self.sequence_amount += 1
        self.current_walk_index = self.sequence_amount
        self.execute_stance_sequence(stance_sequence, crab=crab, interval_index=self.current_walk_index)
        # time.sleep(0.2)

    legs_to_do = {}

    def set_stance(self, stance, crab=False, on_done=lambda: None, enable_ground_clearance=True):
        ax12_serial.lock()
        try:
            for xp, dict in stance.points.items():
                for yp, point in dict.items():
                    leg = self.spider.legs[xp][yp]
                    if enable_ground_clearance:
                        point = Point3D(point.x, point.y - self.ground_clearance, point.z)

                    if stance.midpoints is None:
                        midpoint = None
                    else:
                        midpoint = stance.midpoints[xp]

                    leg.move_to_normalized(point, midpoint, crab)
            threading.Timer(self.spider.interval, on_done).start()
        finally:
            ax12_serial.unlock()

    sequence_amount = 0
    current_walk_index = None

    def execute_stance_sequence(self, stance_list, interval_index=None, index=None, crab=False):
        index = len(stance_list) - 1 if index is None or index == -1 else index

        if interval_index == self.current_walk_index:
            # print("Executing stance sequence:", interval_index)
            self.set_stance(stance_list[index], crab,
                            lambda: self.execute_stance_sequence(stance_list, interval_index, index - 1, crab))
        else:
            print("Sequence %s has been cancelled!" % interval_index)

    def stop(self):
        self.current_walk_index = -1

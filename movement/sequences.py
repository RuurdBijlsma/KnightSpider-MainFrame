from movement.stance import Stance
from point import Point3D

step_length = 100
step_delay = 0.3
step_height = 50
tip_distance = 150

sequences = {
    'walking': [
        (Stance(
            front_left_point=Point3D(tip_distance, 0, step_length / 2),
            mid_left_point=Point3D(tip_distance, 0, -step_length / 2),
            back_left_point=Point3D(tip_distance, 0, step_length / 2),
            front_right_point=Point3D(tip_distance, 0, -step_length / 2),
            mid_right_point=Point3D(tip_distance, 0, step_length / 2),
            back_right_point=Point3D(tip_distance, 0, -step_length / 2)
        ), step_delay),
        (Stance(
            front_left_point=Point3D(tip_distance, 0, -step_length),
            mid_left_point=Point3D(tip_distance, step_height, 0),
            back_left_point=Point3D(tip_distance, 0, -step_length),
            front_right_point=Point3D(tip_distance, step_height, 0),
            mid_right_point=Point3D(tip_distance, 0, -step_length),
            back_right_point=Point3D(tip_distance, step_height, 0)
        ), step_delay),
        (Stance(
            front_left_point=Point3D(tip_distance, 0, -step_length / 2),
            mid_left_point=Point3D(tip_distance, 0, step_length / 2),
            back_left_point=Point3D(tip_distance, 0, -step_length / 2),
            front_right_point=Point3D(tip_distance, 0, step_length / 2),
            mid_right_point=Point3D(tip_distance, 0, -step_length / 2),
            back_right_point=Point3D(tip_distance, 0, step_length / 2)
        ), step_delay),
        (Stance(
            front_left_point=Point3D(tip_distance, step_height, 0),
            mid_left_point=Point3D(tip_distance, 0, -step_length),
            back_left_point=Point3D(tip_distance, step_height, 0),
            front_right_point=Point3D(tip_distance, 0, -step_length),
            mid_right_point=Point3D(tip_distance, step_height, 0),
            back_right_point=Point3D(tip_distance, 0, -step_length)
        ), step_delay),
    ]
}

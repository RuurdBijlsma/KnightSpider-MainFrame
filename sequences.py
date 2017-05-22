from point import Point3D
from stance import Stance

sequences = {
    'walking': [
        (Stance(
            front_left_point=Point3D(150, 0, 50),
            mid_left_point=Point3D(150, 0, -50),
            back_left_point=Point3D(150, 0, 50),
            front_right_point=Point3D(150, 0, -50),
            mid_right_point=Point3D(150, 0, 50),
            back_right_point=Point3D(150, 0, -50)
        ), 1000),
        (Stance(
            front_left_point=Point3D(150, 0, 0),
            mid_left_point=Point3D(150, 20, 0),
            back_left_point=Point3D(150, 0, 0),
            front_right_point=Point3D(150, 20, 0),
            mid_right_point=Point3D(150, 20, 0),
            back_right_point=Point3D(150, 20, 0)
        ), 1000),
        (Stance(
            front_left_point=Point3D(150, 0, -50),
            mid_left_point=Point3D(150, 0, 50),
            back_left_point=Point3D(150, 0, -50),
            front_right_point=Point3D(150, 0, 50),
            mid_right_point=Point3D(150, 0, -50),
            back_right_point=Point3D(150, 0, 50)
        ), 1000),
        (Stance(
            front_left_point=Point3D(150, 20, 0),
            mid_left_point=Point3D(150, 0, 0),
            back_left_point=Point3D(150, 20, 0),
            front_right_point=Point3D(150, 0, 0),
            mid_right_point=Point3D(150, 20, 0),
            back_right_point=Point3D(150, 0, 0)
        ), 1000),
    ]
}

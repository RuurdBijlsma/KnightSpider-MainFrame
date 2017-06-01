import math

from point import Point3D

point = Point3D(4, 4, 4)
origin = Point3D(0, 0, 0)
# point = point.rotate_around_y(angle=math.radians(50))
# point = point.rotate_around_z(angle=math.radians(30))
point = point.rotate_around_x(angle=math.radians(132))

print(point)

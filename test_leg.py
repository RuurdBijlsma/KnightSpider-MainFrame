from inverse_kinematics.actuator import Actuator
from leg import Leg
from point import Point3D
from spider import Spider
from stance import Stance

angle = 60

leg0 = Leg(angle, None)
leg1 = Leg(angle, None)
leg2 = Leg(angle, None)
leg3 = Leg(angle, None)
leg4 = Leg(angle, None)
leg5 = Leg(angle, None)

point0 = Point3D(150, 0, 0)
point1 = Point3D(150, 0, 0)
point2 = Point3D(150, 0, 0)
point3 = Point3D(150, 0, 0)
point4 = Point3D(150, 0, 0)
point5 = Point3D(150, 0, 0)

stance = Stance(point0, point1, point2, point3, point4, point5)
spider = Spider(leg0, leg1, leg2, leg3, leg4, leg5)
spider.leg_mover.set_stance(stance)

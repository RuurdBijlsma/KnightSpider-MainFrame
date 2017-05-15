from inverse_kinematics.actuator import Actuator
from point import Point3D

actuator = Actuator(['y', [80, 0., 0.], 'z', [80, 0., 0.], 'z', [120, 0., 0.]],
                    max_angles=[150, 150, 150],
                    min_angles=[-150, -150, -150])

angles = actuator.inverse_kinematics(Point3D(220, 40, 0))

print("angles: ", angles)

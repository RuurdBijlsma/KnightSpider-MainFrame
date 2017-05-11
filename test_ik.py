from actuator import Actuator
from point import Point3D

actuator = Actuator(['y', [80, 0., 0.], 'z', [80, 0., 0.], 'z', [120, 0., 0.]])
angles = actuator.inverse_kinematics(Point3D(-30, 30, 0))
pos = actuator.forward_kinematics([0, 0, 0])
print("Angles: ", angles)
print("Position: ", pos)

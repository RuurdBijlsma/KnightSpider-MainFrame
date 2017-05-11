from actuator import Actuator
from point import Point3D

actuator = Actuator(['y', [80, 0., 0.], 'z', [80, 0., 0.], 'z', [120, 0., 0.]])
angles = actuator.inverse_kinematics(Point3D(150, -80, 30))
pos = actuator.forward_kinematics([15, 20, 20])
print("Angles: ", angles)
print("Position: ", pos)

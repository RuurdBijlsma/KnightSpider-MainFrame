from actuator import Actuator
from point import Point3D

actuator = Actuator(['y', [65, 0., 0.], 'z', [100, 0., 0.], 'z', [65, 0., 0.]])
angles = actuator.inverse_kinematics(Point3D(-180, 50, -60))
print(angles)

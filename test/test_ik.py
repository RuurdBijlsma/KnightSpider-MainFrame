import websockets.server

from lib.inverse_kinematics.actuator import Actuator
from point import Point3D


def on_message(protocol, message):
    print(protocol, message)


server = websockets.server.serve(on_message, host="141.252.228.164", port=3040)

actuator = Actuator(['y', [80, 0., 0.], 'z', [80, 0., 0.], 'z', [120, 0., 0.]],
                    max_angles=[150, 150, 150],
                    min_angles=[-150, -150, -150])

angles = actuator.inverse_kinematics(Point3D(220, 40, 0))
angles2 = actuator.inverse_kinematics(Point3D(200, -40, 0))

print("angles: ", angles)
print("angles2: ", angles2)

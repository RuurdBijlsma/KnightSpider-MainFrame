import tinyik
import numpy
from point import Point3D


# Todo: X Y Z in arm definition fixen
# modulo 360 doen voor angles

class Actuator:
    def __init__(self, armDefinition):
        for i, val in enumerate(armDefinition): #Fix axes
            if (armDefinition[i] == "z"):
                armDefinition[i] = "y"
            elif (armDefinition[i] == "y"):
                armDefinition[i] = "z"

        self._arm = tinyik.Actuator(armDefinition)

    def inverse_kinematics(self, point):
        self._arm.ee = Actuator.change_format([point.x, point.y, point.z])
        return numpy.rad2deg(self._arm.angles)

    def forward_kinematics(self, angles):
        self._arm.angles = numpy.deg2rad(angles)
        pos = Actuator.change_format(self._arm.ee)
        return Point3D(pos[0], pos[1], pos[2])

    @staticmethod
    def change_format(pos):
        return (-pos[0], -pos[2], -pos[1])

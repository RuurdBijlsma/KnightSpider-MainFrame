import tinyik
import numpy
from point import Point3D


class Arm:
    def __init__(self, armDefinition):
        self._arm = tinyik.Actuator(armDefinition)

    def inverse_kinematics(self, point):
        self._arm.ee = Arm.change_format([point.x, point.y, point.z])
        return numpy.rad2deg(self._arm.angles)

    def forward_kinematics(self, angles):
        self._arm.angles = numpy.deg2rad(angles)
        pos = Arm.change_format(self._arm.ee)
        return Point3D(pos[0], pos[1], pos[2])

    @staticmethod
    def change_format(pos):
        return (-pos[0], -pos[2], -pos[1])

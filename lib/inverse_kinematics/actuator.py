import numpy

from lib.inverse_kinematics.core import TinyActuator
from point import Point3D


class Actuator:
    def __init__(self, armDefinition, max_angles=None, min_angles=None):
        for i, val in enumerate(armDefinition):  # Fix axes
            if (armDefinition[i] == "z"):
                armDefinition[i] = "y"
            elif (armDefinition[i] == "y"):
                armDefinition[i] = "z"

        self._arm = TinyActuator(armDefinition, max_angles=numpy.deg2rad(max_angles), min_angles=numpy.deg2rad(min_angles))

    def inverse_kinematics(self, point):
        self._arm.ee = Actuator.change_format([point.x, point.y, point.z])
        return numpy.rad2deg(self._arm.angles)

    def forward_kinematics(self, angles):
        self._arm.angles = numpy.deg2rad(angles)
        pos = Actuator.change_format(self._arm.ee)
        return Point3D(pos[0], pos[1], pos[2])

    @staticmethod
    def change_format(pos):
        return (pos[0], pos[2], pos[1])

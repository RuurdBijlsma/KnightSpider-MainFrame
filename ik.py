import tinyik
import numpy


class Arm:
    def __init__(self, armDefinition):
        self._arm = tinyik.Actuator(armDefinition)

    def inverseKinematics(self, x, y, z):
        self._arm.ee = Arm.changeFormat([x, y, z])
        return numpy.rad2deg(self._arm.angles)

    def forwardKinematics(self, angles):
        self._arm.angles = numpy.deg2rad(angles)
        pos = Arm.changeFormat(self._arm.ee)
        return {
            'x': pos[0],
            'y': pos[1],
            'z': pos[2]
        }

    @staticmethod
    def changeFormat(pos):
        return (-pos[0], -pos[2], -pos[1])

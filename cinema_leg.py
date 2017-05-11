import c4d
import numpy
from actuator import Actuator


class CinemaLeg(object):
    ALPHA_ID = "alpha"
    BETA_ID = "beta"
    GAMMA_ID = "gamma"

    def __init__(self, serial_connection):
        self.serial_connection = serial_connection
        self.actuator = Actuator(['y', [80, 0., 0.], 'z', [80, 0., 0.], 'z', [120, 0., 0.]])
        document = c4d.documents.GetActiveDocument()
        self.gamma = document.SearchObject("gamma")
        self.alpha = document.SearchObject("alpha")
        self.beta = document.SearchObject("beta")

    def move_to(self, point):
        angles = numpy.deg2rad(self.actuator.inverse_kinematics(point))
        print("angles", angles)
        self.gamma[c4d.ID_BASEOBJECT_REL_ROTATION, c4d.VECTOR_X] = 0
        self.alpha[c4d.ID_BASEOBJECT_REL_ROTATION, c4d.VECTOR_Z] = 0
        self.beta[c4d.ID_BASEOBJECT_REL_ROTATION, c4d.VECTOR_Z] = 0

from arm import Arm


class Leg(object):
    ALPHA_ID = 1
    BETA_ID = 2
    GAMMA_ID = 3

    ROTATION_SPEED = 512

    def __init__(self, serial_connection):
        self.serial_connection = serial_connection
        self.kinematic_arm = Arm(['z', [65, 0., 0.], 'y', [100, 0., 0.], 'y', [65, 0., 0.]])

    def move_to(self, point):
        angles = self.kinematic_arm.inverse_kinematics(point)
        self.rotate_servo(self.GAMMA_ID, angles[0])
        self.rotate_servo(self.ALPHA_ID, angles[1])
        self.rotate_servo(self.BETA_ID, angles[2])

    def rotate_servo(self, id, angle):
        self.serial_connection.goto(id, angle, speed=self.ROTATION_SPEED, degrees=True)

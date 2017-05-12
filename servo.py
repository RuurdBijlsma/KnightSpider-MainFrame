import time


class Servo(object):

    ROTATION_SPEED = 512

    def __init__(self, serial_connection, id, min_angle=150, max_angle=150, flip_angles = False):
        self.flip_angles = flip_angles
        self.serial_connection = serial_connection
        self.max_angle = max_angle
        if(self.max_angle > 150):
            self.max_angle = 150
        self.min_angle = min_angle
        if(self.min_angle > 150):
            self.min_angle = 150
        self.id = id

    def rotate(self, angle):
        if angle < self.min_angle:
            angle = self.min_angle
        elif angle > self.max_angle:
            angle = self.max_angle

        if(self.flip_angles):
            angle *= -1

        angle = int(angle)

        print("Rotating servo {0} to {1}".format(self.id, angle))

        try:
            self.serial_connection.goto(self.id, angle, speed=self.ROTATION_SPEED, degrees=True)
        except ValueError as e:
            print("Error moving servo", e)

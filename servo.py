import time


class Servo(object):

    ROTATION_SPEED = 512

    def __init__(self, serial_connection, id, min_angle, max_angle):
        self.serial_connection = serial_connection
        self.max_angle = max_angle
        self.min_angle = min_angle
        self.id = id

    def rotate(self, angle):
        if angle < self.min_angle:
            angle = self.min_angle
        elif angle > self.max_angle:
            angle = self.max_angle

        angle = int(angle)

        print("Rotating servo {0} to {1}".format(self.id, angle))

        try:
            self.serial_connection.goto(self.id, angle, speed=self.ROTATION_SPEED, degrees=True)
        except ValueError as e:
            print("Error moving servo", e)

        time.sleep(0.1)




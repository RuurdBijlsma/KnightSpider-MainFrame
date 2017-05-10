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

        self.serial_connection.goto(id, angle, speed=self.ROTATION_SPEED, degrees=True)




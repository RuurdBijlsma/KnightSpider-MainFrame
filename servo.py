import time
import ax12_serial

class ServoReadings(object):
    def __init__(self, id, position = -1, speed = -1, load = -1, voltage = -1, temperature = -1):
        self.id = id
        self.temperature = temperature
        self.voltage = voltage
        self.load = load
        self.speed = speed
        self.position = position

    def __str__(self):
        return "Readings for {5}:\nTemperature = {0}\nVoltage = {1}\nLoad = {2}\nSpeed = {3}\nPosition = {4}\n".format(
            self.temperature,
            self.voltage,
            self.load,
            self.speed,
            self.position,
            self.id
        )


class Servo(object):

    ROTATION_SPEED = 400

    def __init__(self, serial_connection, id, offset_angle=0, min_angle=-150, max_angle=150, flip_angles=False):
        self.flip_angles = flip_angles
        self.serial_connection = serial_connection
        self.max_angle = max_angle
        self.offset_angle = offset_angle
        if (self.max_angle > 150):
            self.max_angle = 150
        self.min_angle = min_angle
        if (self.min_angle < -150):
            self.min_angle = -150
        self.id = id

    def rotate_to(self, angle):
        if angle < self.min_angle:
            angle = self.min_angle
        elif angle > self.max_angle:
            angle = self.max_angle

        if (self.flip_angles):
            angle *= -1

        angle += self.offset_angle

        angle = int(angle)

        print("Rotating servo {0} to {1}".format(self.id, angle))

        try:
            ax12_serial.rotate_to(self.id, angle, speed=self.ROTATION_SPEED, degrees=True)
        except ValueError as e:
            print("Error moving servo:", e)
            # raise e

    def get_readings(self):
        try:
            return ServoReadings(
                position=ax12_serial.read_position(self.id),
                speed=ax12_serial.read_speed(self.id),
                voltage=ax12_serial.read_voltage(self.id),
                temperature=ax12_serial.read_temperature(self.id),
                load=ax12_serial.read_load(self.id),
                id=self.id,
            )
        except TypeError as e:
            print("Error reading from servo:", e)

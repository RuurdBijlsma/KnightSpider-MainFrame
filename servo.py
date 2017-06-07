import threading

import ax12_serial
from models import ServoReadings


class Servo(object):
    ROTATION_SPEED = 1000
    ANGLE_THRESHOLD = 3
    TIMER_DELAY = 0.1

    def __init__(self, id, offset_angle=0, min_angle=-150, max_angle=150, flip_angles=False):
        self.flip_angles = flip_angles
        self.max_angle = max_angle
        self.offset_angle = offset_angle
        if (self.max_angle > 150):
            self.max_angle = 150
        self.min_angle = min_angle
        if (self.min_angle < -150):
            self.min_angle = -150
        self.id = id

        self._cached_readings = ServoReadings(
            position=0,
            voltage=0,
            temperature=0,
            load=0,
            id=id,
        )

    def rotate_to(self, angle, on_done=lambda: None):
        if angle < self.min_angle:
            angle = self.min_angle
        elif angle > self.max_angle:
            angle = self.max_angle

        if (self.flip_angles):
            angle *= -1

        angle += self.offset_angle

        angle = int(angle)

        # print("Rotating servo {0} to {1}".format(self.id, angle))

        try:
            ax12_serial.rotate_to(self.id, angle, speed=self.ROTATION_SPEED, degrees=True)
        except ValueError as e:
            print("Error moving servo:", e)

        threading.Timer(self.TIMER_DELAY, on_done).start()

    def update_readings(self):
        self._cached_readings = self.get_readings()

    @property
    def readings(self):
        return self._cached_readings

    @property
    def angle(self):
        return self._cached_readings.position

    def get_readings(self):
        try:
            readings = ServoReadings(
                position=ax12_serial.read_position(self.id),
                voltage=ax12_serial.read_voltage(self.id),
                temperature=ax12_serial.read_temperature(self.id),
                load=ax12_serial.read_load(self.id),
                id=self.id,
            )
            return readings
        except TypeError as e:
            # print("Error reading from servo:", e)
            return ServoReadings.empty()

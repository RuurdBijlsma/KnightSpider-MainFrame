import threading

import ax12_serial
from models import ServoReadings

TRANING_MODE=False

class Servo(object):
    def __init__(self, id, offset_angle=0, min_angle=-150, max_angle=150, flip_angles=False, move_speed=300,
                 step_interval=0.1):
        self.flip_angles = flip_angles
        self.max_angle = max_angle
        self.offset_angle = offset_angle
        if (self.max_angle > 150):
            self.max_angle = 150
        self.min_angle = min_angle
        if (self.min_angle < -150):
            self.min_angle = -150
        self.id = id

        self.move_speed = move_speed
        self.step_interval = step_interval

        self._cached_readings = ServoReadings(
            position=0,
            voltage=0,
            temperature=0,
            load=0,
            id=id,
        )

    def rotate_to(self, angle):
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
            # pass
            if not TRANING_MODE:
                ax12_serial.rotate_to(self.id, angle, speed=self.move_speed, degrees=True)
        except ValueError as e:
            print("Error moving servo:", e)

    def update_readings(self):
        self._cached_readings = self.get_readings()

    @property
    def readings(self):
        return self._cached_readings

    @property
    def angle(self):
        return self._cached_readings.position

    def get_readings(self):
        ax12_serial.lock()
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
        finally:
            ax12_serial.unlock()

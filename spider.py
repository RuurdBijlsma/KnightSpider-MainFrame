import json
import math

import utils
from leg import Leg
from models import SpiderInfo
from movement.ik_cache import IKCache
from movement.leg_mover import LegMover
from point import Point3D


class Spider(object):
    def __init__(self):
        self.ik_cache = IKCache('store/ik_cache.json')
        self.ik_cache.from_file()
        # self.ik_cache.clear()

        # legs = [
        #     Leg(self.ik_cache, leg_id=1, angle=30, body_position=Point3D(-70.8, 0, 104.12)),
        #     Leg(self.ik_cache, leg_id=2, angle=0, body_position=Point3D(-83, 0, 0)),
        #     Leg(self.ik_cache, leg_id=3, angle=-30, body_position=Point3D(-71.09, 0, -108.50)),
        #     Leg(self.ik_cache, leg_id=4, angle=-30, body_position=Point3D(69.8, 0, 103.65)),
        #     Leg(self.ik_cache, leg_id=5, angle=0, body_position=Point3D(83, 0, 0)),
        #     Leg(self.ik_cache, leg_id=6, angle=30, body_position=Point3D(69.58, 0, -108.97)),
        # ]

        legs = [
            Leg(self.ik_cache, leg_id=1, angle=0, body_position=Point3D(-70.8, 0, 104.12)),
            Leg(self.ik_cache, leg_id=2, angle=0, body_position=Point3D(-83, 0, 0)),
            Leg(self.ik_cache, leg_id=3, angle=0, body_position=Point3D(-71.09, 0, -108.50)),
            Leg(self.ik_cache, leg_id=4, angle=0, body_position=Point3D(69.8, 0, 103.65)),
            Leg(self.ik_cache, leg_id=5, angle=0, body_position=Point3D(83, 0, 0)),
            Leg(self.ik_cache, leg_id=6, angle=0, body_position=Point3D(69.58, 0, -108.97)),
        ]

        self.legs = {
            'left': {
                'front': legs[0],
                'mid': legs[1],
                'back': legs[2]
            },
            'right': {
                'front': legs[3],
                'mid': legs[4],
                'back': legs[5]
            }
        }
        self.leg_mover = LegMover(self, ground_clearance=50)

    def rotate_body(self, x_angle, z_angle):
        for leg in self.leg_iter:
            just_the_tip = leg.get_body_to_tip_point()
            tip_y = just_the_tip.y
            rotated = just_the_tip.rotate_around_x(angle=x_angle)
            rotated = rotated.rotate_around_z(angle=z_angle)
            gho = tip_y - rotated.y
            leg.ground_height_offset = gho

    @property
    def cpu_temperature(self):
        return self._cpu_temperature

    @cpu_temperature.setter
    def cpu_temperature(self, value):
        self._cpu_temperature = value

    @property
    def cpu_usage(self):
        return self._cpu_usage

    @cpu_usage.setter
    def cpu_usage(self, value):
        self._cpu_usage = value

    def update_readings(self):
        for leg in self.leg_iter:
            leg.update_readings()

    @property
    def leg_iter(self):
        for value in self.legs.values():
            for leg in value.values():
                yield leg

    @property
    def servo_iter(self):
        for leg in self.leg_iter:
            yield leg.gamma
            yield leg.beta
            yield leg.alpha

    def get_servo_by_id(self, id):
        for servo in self.servo_iter:
            if servo.id == id:
                return servo

    def get_servo_angles(self):
        result = {}

        for leg in self.leg_iter:
            for reading in leg.readings:
                result[reading.id] = reading.position

        return result

    def get_servo_angles_json(self):
        return json.dumps(self.get_servo_angles(), separators=(",", ":"))

    def get_servo_readings_json(self):
        return json.dumps({k: v.to_json() for k, v in self.get_servo_readings_flat().items()}, separators=(",", ":"))

    def get_servo_readings_flat(self):
        result = {}

        for leg in self.leg_iter:
            for reading in leg.readings:
                result[reading.id] = reading

        return result

    def get_servo_readings(self):
        return {
            'left': {
                'front': self.legs['left']['front'].readings,
                'mid': self.legs['left']['mid'].readings,
                'back': self.legs['left']['back'].readings
            },
            'right': {
                'front': self.legs['right']['front'].readings,
                'mid': self.legs['right']['mid'].readings,
                'back': self.legs['right']['back'].readings
            }
        }

    def get_info(self):
        return SpiderInfo(
            battery_level=200,
            slope=20,
            cpu_usage=utils.get_cpu_usage(),
            cpu_temperature=utils.get_cpu_temp()
        )

    def start(self):
        self.leg_mover.walk(rotate_angle=math.radians(0), step_height=0, step_length=0, tip_distance=120,
                            turn_modifier=0)

    @property
    def step_height(self):
        return self._step_height

    @step_height.setter
    def step_height(self, value):
        self._step_height = value
        self.update_spider()

    @property
    def rotate_angle(self):
        return self._rotate_angle

    @rotate_angle.setter
    def rotate_angle(self, value):
        self._rotate_angle = value
        self.update_spider()

    @property
    def step_length(self):
        return self._step_length

    @step_length.setter
    def step_length(self, value):
        self._step_length = value
        self.update_spider()

    @property
    def tip_distance(self):
        return self._tip_distance

    @tip_distance.setter
    def tip_distance(self, value):
        self._tip_distance = value
        self.update_spider()

    @property
    def turn_modifier(self):
        return self._turn_modifier

    @turn_modifier.setter
    def turn_modifier(self, value):
        self._turn_modifier = value
        self.update_spider()

    def update_spider(self):
        self.leg_mover.walk(rotate_angle=self.rotate_angle, step_height=self.step_height, step_length=self.step_length,
                            tip_distance=self.tip_distance, turn_modifier=self.turn_modifier)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        max_servo_speed = 1023
        interval_at_max_speed = 0.1
        interval = max_servo_speed * interval_at_max_speed / value
        self._speed = value
        for servo in self.servo_iter:
            servo.move_speed = value
            servo.step_interval = interval

    def parse_controller_update(self, data):
        max_stick_value = 14000
        stick_x, stick_y, mode, *pressed_buttons = data.split(",")
        print(stick_x, stick_y, mode, pressed_buttons)
        stick_x /= max_stick_value
        stick_y /= max_stick_value
        try:
            {
                0: lambda: self.manual_mode((stick_x, stick_y), pressed_buttons),
                1: lambda: self.egg_mode(),
            }[mode]()
        except:
            print("Mode doesn't exist")

    def manual_mode(self, stick, buttons):
        print("[MANUAL]", stick, buttons)

    def egg_mode(self):
        print("[EGG]")

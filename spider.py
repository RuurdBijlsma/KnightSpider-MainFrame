import json
import os
from threading import Thread

import math
import signal

import egg_maw
import utils
from leg import Leg
from models import SpiderInfo
from movement.ik_cache import IKCache
from movement.leg_mover import LegMover
from pistreaming.server import Server
from point import Point3D
from socket_listener.app_communicator import AppCommunicator


class Spider(object):
    def __init__(self):
        self.ik_cache = IKCache('store/ik_cache.json')
        self.ik_cache.from_file()
        # self.ik_cache.clear()

        legs = [
            Leg(self.ik_cache, leg_id=1, angle=-30, body_position=Point3D(-70.8, 0, 104.12)),
            Leg(self.ik_cache, leg_id=2, angle=0, body_position=Point3D(-83, 0, 0)),
            Leg(self.ik_cache, leg_id=3, angle=30, body_position=Point3D(-71.09, 0, -108.50)),
            Leg(self.ik_cache, leg_id=4, angle=30, body_position=Point3D(69.8, 0, 103.65)),
            Leg(self.ik_cache, leg_id=5, angle=0, body_position=Point3D(83, 0, 0)),
            Leg(self.ik_cache, leg_id=6, angle=-30, body_position=Point3D(69.58, 0, -108.97)),
        ]

        # legs = [
        #     Leg(self.ik_cache, leg_id=1, angle=0, body_position=Point3D(-70.8, 0, 104.12)),
        #     Leg(self.ik_cache, leg_id=2, angle=0, body_position=Point3D(-83, 0, 0)),
        #     Leg(self.ik_cache, leg_id=3, angle=0, body_position=Point3D(-71.09, 0, -108.50)),
        #     Leg(self.ik_cache, leg_id=4, angle=0, body_position=Point3D(69.8, 0, 103.65)),
        #     Leg(self.ik_cache, leg_id=5, angle=0, body_position=Point3D(83, 0, 0)),
        #     Leg(self.ik_cache, leg_id=6, angle=0, body_position=Point3D(69.58, 0, -108.97)),
        # ]

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
        self.leg_mover = LegMover(self)
        signal.signal(signal.SIGINT, self.sigint_handler)

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

    def start(self, all_systems_enabled=True):
        self.all_systems_enabled = all_systems_enabled
        self.leg_mover.ground_clearance = 80
        self.speed = 300
        self.interval_at_max_speed = 0.06

        self.rotate_angle = math.radians(90)
        self.step_height = 50
        self.step_length = 0
        self.tip_distance = 120
        self.turn_modifier = 1
        self.crab = True

        self.rotate_body(x_angle=math.radians(0), z_angle=math.radians(0))

        self.update_spider()

        egg_maw.init()
        egg_maw.open_maw()

        if all_systems_enabled:
            # speech_synthesis.speak("Starting all systems")
            self.app = AppCommunicator(self, False)
            self.stream_server = Server()
            Thread(target=self.stream_server.start)

    def close(self):
        try:
            self.speed = 0
            self.app.close()
            self.stream_server.close()
            egg_maw.close()
        except:
            pass

    def sigint_handler(self, sig, frame):
        print("Received SIGINT, cleaning up")
        self.close()

        print("killing")
        os.kill(os.getpid(), signal.SIGTERM)

    @property
    def step_height(self):
        return self._step_height

    @step_height.setter
    def step_height(self, value):
        self._step_height = value

    @property
    def rotate_angle(self):
        return self._rotate_angle

    @rotate_angle.setter
    def rotate_angle(self, value):
        self._rotate_angle = value

    @property
    def step_length(self):
        return self._step_length

    @step_length.setter
    def step_length(self, value):
        self._step_length = value

    @property
    def tip_distance(self):
        return self._tip_distance

    @tip_distance.setter
    def tip_distance(self, value):
        self._tip_distance = value

    @property
    def turn_modifier(self):
        return self._turn_modifier

    @turn_modifier.setter
    def turn_modifier(self, value):
        self._turn_modifier = value

    def update_spider(self):
        self.leg_mover.walk(rotate_angle=self.rotate_angle, step_height=self.step_height, step_length=self.step_length,
                            tip_distance=self.tip_distance, turn_modifier=self.turn_modifier, crab=self.crab)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        max_servo_speed = 1023
        interval = max_servo_speed * self.interval_at_max_speed / value
        self._speed = value
        for servo in self.servo_iter:
            servo.move_speed = value
            servo.step_interval = interval

    def parse_controller_update(self, data):
        max_stick_value = 14000
        stick_y, stick_x, up, down, left, right, joystick_button, mode = [int(value) for value in data.split(",")]
        stick_x /= max_stick_value
        stick_y /= max_stick_value
        {
            1: lambda: self.fury_mode(),
            2: lambda: self.manual_mode((stick_x, stick_y), 1 if up == 1 else -1 if down == 1 else 0,
                                        1 if right == 1 else -1 if left == 1 else 0),
            3: lambda: self.dance_mode(),
            4: lambda: self.egg_mode(),
            5: lambda: self.balloon_mode(),
            6: lambda: self.line_dance_mode(),
        }[mode]()

    def manual_mode(self, stick, vertical, horizontal):
        stick = [round(value * 5) / 5 for value in stick]
        print(stick, vertical, horizontal)
        max_step_length = 110
        min_step_height = 40
        step_height_deviation = 20
        height_change_multiplier = 5
        turn_threshold = 0.1
        minimum_threshold = 5

        x, y = stick

        self.leg_mover.ground_clearance += vertical * height_change_multiplier

        step_length = math.sqrt(x ** 2 + y ** 2) * max_step_length
        # step length is meer als de joystick verder van het midden af is
        rotate_angle = math.radians(180 if y > 0 else 0)
        step_height = 0 if step_length < minimum_threshold else min_step_height + abs(y) * step_height_deviation

        turn_modifier = float(1 if x > turn_threshold else -1 if x < -turn_threshold else 0)
        turn_modifier = turn_modifier - abs(y * 0.5) if turn_modifier > 0.5 else turn_modifier + abs(
            y * 0.5) if turn_modifier < -0.5 else turn_modifier

        change = False

        if step_length != self.step_length:
            self.step_length = step_length
            change = True
        if rotate_angle != self.rotate_angle:
            self.rotate_angle = rotate_angle
            change = True
        if step_height != self.step_height:
            self.step_height = step_height
            change = True
        if turn_modifier != self.turn_modifier:
            self.turn_modifier = turn_modifier
            change = True

        if (change):
            print({
                "turnModifier": self.turn_modifier,
                "stepLength": self.step_length,
                "stepHeight": self.step_height,
                "rotateAngle": self.rotate_angle,
            })
            # print(change)
            self.update_spider()

    def fury_mode(self):
        pass

    def dance_mode(self):
        pass

    def egg_mode(self):
        pass

    def balloon_mode(self):
        pass

    def line_dance_mode(self):
        pass

    def cache_controller_ik(self, stick_divider=5, height_step=5, min_height=30, max_height=160):
        for x in range(-stick_divider, stick_divider):
            for y in range(-stick_divider, stick_divider):
                self.manual_mode((x / stick_divider, y / stick_divider), 0, 0)

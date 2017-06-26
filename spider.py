import json
import math
import os
import signal
import time

import numpy as np

import distance
import egg_maw
import movement.dance_sequence as dance_sequence
import utils
from gyroscoop import Gyroscoop
from leg import Leg
from models import SpiderInfo
from movement.dance_mover import DanceMover
from movement.ik_cache import IKCache
from movement.leg_mover import LegMover
from point import Point3D
from socket_listener.app_communicator import AppCommunicator
from vision import cards
from vision import magic
from vision import road_detector
from visionclass import Vision


class Spider(object):
    def __init__(self):
        self.ik_cache = IKCache('store/ik_cache.json')
        self.ik_cache.from_file()
        # self.ik_cache.clear()

        legs = [
            Leg(self.ik_cache, leg_id=1, angle=-30, body_position=Point3D(-70.8, 0, 104.12)),
            Leg(self.ik_cache, leg_id=2, angle=0, body_position=Point3D(-83, 0, 0)),
            Leg(self.ik_cache, leg_id=3, angle=30, body_position=Point3D(-70.8, 0, -104.12)),
            Leg(self.ik_cache, leg_id=4, angle=30, body_position=Point3D(70.8, 0, 104.12)),
            Leg(self.ik_cache, leg_id=5, angle=0, body_position=Point3D(83, 0, 0)),
            Leg(self.ik_cache, leg_id=6, angle=-30, body_position=Point3D(70.8, 0, -104.12)),
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
                'front': legs[5],
                'mid': legs[4],
                'back': legs[3]
            },
            'right': {
                'front': legs[0],
                'mid': legs[1],
                'back': legs[2]
            }
        }

        self.interval_at_max_speed = 0.1

        self.leg_mover = LegMover(self)
        self.dance_mover = DanceMover(self, dance_sequence.create_sayora_maxwell_dance(self))
        signal.signal(signal.SIGINT, self.sigint_handler)

    def rotate_body(self, x_angle, z_angle):
        self.rotate_x = x_angle
        self.rotate_z = z_angle
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
            slope=self.gyroscope.get_x_rotation(self.gyroscope.read_gyro()),
            cpu_usage=utils.get_cpu_usage(),
            cpu_temperature=utils.get_cpu_temp()
        )

    def start(self, all_systems_enabled=True):
        self.all_systems_enabled = all_systems_enabled
        self.leg_mover.ground_clearance = 100
        self.interval_at_max_speed = 0.1
        self.speed = 1000

        self.rotate_angle = math.radians(180)
        self.step_height = 0
        self.step_length = 0
        self.tip_distance = 120
        self.turn_modifier = 0
        self.crab = False

        self.rotate_body(math.radians(0), math.radians(0))

        self.update_walk(self.stats_dict[magic.CENTER])

        self.gyroscope = Gyroscoop()

        egg_maw.init()
        egg_maw.open_maw()

        distance.init()

        self.vision = Vision()

        if all_systems_enabled:
            # self.speech_synthesis = SpeechSynthesis()
            # self.speech_synthesis.speak("Starting all systems")
            self.app = AppCommunicator(self, False)

    def close(self):
        try:
            self.speed = 0
            self.app.close()
            # self.stream_server.close()
            self.vision.close()
            egg_maw.close()
        except:
            pass

    def sigint_handler(self, sig, frame):
        print("Received SIGINT, cleaning up")
        self.close()

        print("killing")
        os.kill(os.getpid(), signal.SIGTERM)

    def update_walk(self, stats):
        self.current_stats = stats
        self.leg_mover.walk(rotate_angle=stats['rotate_angle'],
                            step_height=stats['step_height'],
                            step_length=stats['step_length'],
                            tip_distance=stats['tip_distance'],
                            turn_modifier=stats['turn_modifier'],
                            crab=stats['crab'])

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        max_servo_speed = 1023
        self.interval = max_servo_speed * self.interval_at_max_speed / value
        self._speed = value
        for servo in self.servo_iter:
            servo.move_speed = value
            servo.step_interval = self.interval

    def parse_controller_update(self, data):
        if data == "stop":
            return

        max_stick_value = 14000
        stick_y, stick_x, up_button, down_button, left_button, right_button, joystick_button, mode = [int(value) for
                                                                                                      value in
                                                                                                      data.split(",")]
        stick_x /= max_stick_value
        stick_y /= max_stick_value
        {
            1: lambda: self.fury_mode(),
            2: lambda: self.manual_mode((stick_x, stick_y), 1 if up_button == 1 else -1 if down_button == 1 else 0,
                                        bool(left_button), bool(right_button), bool(joystick_button)),
            3: lambda: self.dance_mode(),
            4: lambda: self.egg_mode(cards.CLUB, True),
            5: lambda: self.balloon_mode(),
            6: lambda: self.line_dance_mode(),
        }[mode]()

    def lowrider_mode(self, stick):
        rotation_speed_multiplier = 0.01
        print("not implementede error")
        # self.rotate_x += stick[0] * rotation_speed_multiplier
        # self.rotate_z += stick[1] * rotation_speed_multiplier

    current_stats = {}
    tip_distance = {
        'forward': 120,
        'crab': 120
    }
    step_length = 60
    step_height = 40
    stats_dict = {
        magic.CENTER: {
            'step_length': 0,
            'tip_distance': tip_distance['forward'],
            'step_height': 0,
            'rotate_angle': math.radians(180),
            'turn_modifier': 0,
            'crab': False,
        },
        magic.UP: {
            'step_length': step_length,
            'tip_distance': tip_distance['forward'],
            'step_height': step_height,
            'rotate_angle': math.radians(180),
            'turn_modifier': 0,
            'crab': False,
        },
        magic.DOWN: {
            'step_length': step_length,
            'tip_distance': tip_distance['forward'],
            'step_height': step_height,
            'rotate_angle': math.radians(0),
            'turn_modifier': 0,
            'crab': False,
        },
        magic.RIGHT: {
            'step_length': step_length,
            'tip_distance': tip_distance['crab'],
            'step_height': step_height,
            'rotate_angle': math.radians(90),
            'turn_modifier': 1,
            'crab': True,
        },
        magic.LEFT: {
            'step_length': step_length,
            'tip_distance': tip_distance['crab'],
            'step_height': step_height,
            'rotate_angle': math.radians(-90),
            'turn_modifier': 1,
            'crab': True,
        },
        magic.ROTATE_RIGHT: {
            'step_length': step_length,
            'tip_distance': tip_distance['forward'],
            'step_height': step_height,
            'rotate_angle': math.radians(0),
            'turn_modifier': 1,
            'crab': False,
        },
        magic.ROTATE_LEFT: {
            'step_length': step_length,
            'tip_distance': tip_distance['forward'],
            'step_height': step_height,
            'rotate_angle': math.radians(0),
            'turn_modifier': -1,
            'crab': False,
        },
        magic.TURN_RIGHT: {
            'step_length': step_length,
            'tip_distance': tip_distance['forward'],
            'step_height': step_height,
            'rotate_angle': math.radians(180),
            'turn_modifier': 0.25,
            'crab': False,
        },
        magic.TURN_LEFT: {
            'step_length': step_length,
            'tip_distance': tip_distance['forward'],
            'step_height': step_height,
            'rotate_angle': math.radians(180),
            'turn_modifier': -0.25,
            'crab': False,
        },
    }

    def manual_mode(self, stick, vertical, left_button, right_button, joystick_button):
        height_multiplier = 10

        if (joystick_button):
            rotate_multiplier = math.radians(5)
            self.rotate_body(self.rotate_x + vertical * rotate_multiplier, self.rotate_z)
        else:
            self.leg_mover.ground_clearance += vertical * height_multiplier

        y, x = utils.rotate((0, 0), stick, math.radians(30))
        y *= -1
        threshold = 0.1
        rotation = magic.ROTATE_LEFT if left_button else magic.ROTATE_RIGHT if right_button else magic.CENTER
        direction = magic.UP if y > x and y > threshold else magic.DOWN if y < x and y < -threshold else magic.LEFT if x > y and x > threshold else  magic.RIGHT if x < y and x < -threshold else magic.CENTER

        if rotation == magic.CENTER or direction == magic.LEFT or direction == magic.RIGHT:
            stats = self.stats_dict[direction]
        elif direction == magic.CENTER:
            stats = self.stats_dict[rotation]
        else:
            if (direction == magic.UP and rotation == magic.ROTATE_RIGHT):
                stats = self.stats_dict[magic.TURN_RIGHT]
            elif (direction == magic.UP and rotation == magic.ROTATE_LEFT):
                stats = self.stats_dict[magic.TURN_LEFT]
            else:
                stats = self.stats_dict[magic.CENTER]

        if stats != self.current_stats:
            print({
                      magic.UP: "UP",
                      magic.DOWN: "DOWN",
                      magic.RIGHT: "RIGHT",
                      magic.LEFT: "LEFT",
                      magic.CENTER: "CENTER",
                      magic.ROTATE_LEFT: "ROTATE_LEFT",
                      magic.ROTATE_RIGHT: "ROTATE_RIGHT",
                      magic.TURN_LEFT: "TURN_LEFT",
                      magic.TURN_RIGHT: "TURN_RIGHT",
                  }[direction])
            if not joystick_button:
                self.update_walk(stats)

    is_on_circle = False
    lock_fury = False

    def fury_mode(self):
        wait_time_on_circle = 30
        # position = self.vision.find_road()
        # if position == magic.CENTER:
        if self.is_on_circle and not self.lock_fury:
            print("past circle")
            self.move_forward()
        else:
            if road_detector.is_circle_on_screen(self.vision.server.get_capture()):
                print("moving towards circle")
                self.move_forward()
            else:
                self.is_on_circle = True
                self.lock_fury = True
                self.go_direction(magic.CENTER)
                print("circle no longer in view")
                time.sleep(wait_time_on_circle)
                self.lock_fury = False
                # else:
                #     self.move_to_magic(position)

    def dance_mode(self):
        print("evacueer de dansvloer")
        if not self.dance_mover.is_playing:
            print("lekker beginnen")
            self.leg_mover.stop()
            print("gestupt")
            self.dance_mover.execute()
            print("dans execute")

    def egg_mode(self, card, colored):
        self.speed = 200
        # if egg_maw.current_pwm == egg_maw.OPEN_PWM:
        #     if colored:
        #         position = self.vision.find_colored_egg()
        #         self.operate_maw(False, position)
        #     else:
        #         position = self.vision.find_white_egg()
        #         self.operate_maw(False, position)
        # else:
        if card == cards.SPADE:
            position = self.vision.find_spades()
            self.operate_maw(True, position)
        elif card == cards.CLUB:
            position = self.vision.find_club()
            self.operate_maw(True, position)
        elif card == cards.HART:
            position = self.vision.find_heart()
            self.operate_maw(True, position)
        else:
            position = self.vision.find_diamond()
            self.operate_maw(True, position)

    def balloon_mode(self, stick, _, left_button, right_button, __):
        # Call manual mode with a few options preset
        self.leg_mover.ground_clearance = 140
        self.rotate_body(0, math.radians(-50))
        self.manual_mode(stick, 0, left_button, right_button, 0)

    def hill_mode(self, stick, vertical, left_button, right_button, joystick_button):
        # Call manual mode with a few options preset
        self.leg_mover.ground_clearance = 140
        self.balance()
        self.manual_mode(stick, 0, left_button, right_button, 0)

    def gap_mode(self, stick, vertical, left_button, right_button, joystick_button):
        # Call manual mode with a few options preset
        self.leg_mover.ground_clearance = 50
        self.speed = 100
        self.manual_mode(stick, 0, left_button, right_button, 0)

    def line_dance_mode(self):
        pass

    def operate_maw(self, open, position):
        if position == magic.CENTER:
            if 10 < distance.get_distance():
                print("moving forward towards target")
                self.move_to_magic(position)
            elif distance is not float("inf"):
                if open:
                    egg_maw.open_maw()
                else:
                    egg_maw.close_maw()
        else:
            self.move_to_magic(position)

    def move_to_magic(self, magic_number):
        {
            magic.CENTER: lambda: self.move_forward(),
            magic.LEFT: lambda: self.turn_left(),
            magic.RIGHT: lambda: self.turn_right(),
        }[magic_number]()

    def go_direction(self, direction):
        print("ik mot draaie", magic.KEYS[direction])
        stats = self.stats_dict[direction]
        if stats != self.current_stats:
            print("heus")
            self.update_walk(stats)

    def turn_left(self):
        self.go_direction(magic.ROTATE_LEFT)

    def turn_right(self):
        self.go_direction(magic.ROTATE_RIGHT)

    def move_forward(self):
        self.go_direction(magic.UP)

    def move_backward(self):
        self.go_direction(magic.DOWN)

    def stand_tilted(self, x, y):
        self.rotate_body(math.radians(x), math.radians(y))
        self.leg_mover.stop()
        self.update_walk(self.stats_dict[magic.CENTER])

    def stand_tilted_x(self, angle):
        self.rotate_body(math.radians(angle), 0)
        self.leg_mover.stop()
        self.update_walk(self.stats_dict[magic.CENTER])

    def stand_tilted_y(self, angle):
        self.rotate_body(0, math.radians(angle))
        self.leg_mover.stop()
        self.update_walk(self.stats_dict[magic.CENTER])

    @property
    def gyro_angle(self):
        return self.gyroscope.get_y_rotation(self.gyroscope.read_gyro())

    calibrated_angle = -1.5
    angle_history = []

    def balance(self):
        round_to_nearest = 2
        avg_items = 5

        raw_angle = self.gyro_angle - self.calibrated_angle
        raw_angle = round(raw_angle / round_to_nearest) * round_to_nearest

        body_angle = math.degrees(self.rotate_x)
        print("Gyro angle: ", raw_angle, "Body angle:", body_angle)
        angle = -raw_angle

        self.angle_history.append(angle)
        self.angle_history = self.angle_history[-avg_items:]

        self.rotate_body(math.radians(np.average(self.angle_history)), 0)

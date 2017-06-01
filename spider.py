import json

from movement.ik_cache import IKCache
from movement.leg_mover import LegMover

import utils
from leg import Leg
from models import SpiderInfo


class Spider(object):
    def __init__(self):
        self.ik_cache = IKCache('store/ik_cache.json')
        self.ik_cache.from_file()
        # self.ik_cache.clear()

        legs = [
            Leg(self.ik_cache, leg_id=1, angle=-30),
            Leg(self.ik_cache, leg_id=2, angle=0),
            Leg(self.ik_cache, leg_id=3, angle=30),
            Leg(self.ik_cache, leg_id=4, angle=-30),
            Leg(self.ik_cache, leg_id=5, angle=0),
            Leg(self.ik_cache, leg_id=6, angle=30),
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

    def get_servo_angles(self):
        result = {}

        for leg in self.leg_iter:
            for reading in leg.readings:
                result[reading.id] = reading.position

        return result

    def get_servo_angles_json(self):
        return json.dumps(self.get_servo_angles(), separators=(",", ":"))

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

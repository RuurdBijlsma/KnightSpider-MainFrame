import utils
from movement.leg_mover import LegMover


class Spider(object):
    def __init__(self, front_left_leg, mid_left_leg, back_left_leg, back_right_leg, mid_right_leg, front_right_leg):
        self.legs = {
            'left': {
                'front': front_left_leg,
                'mid': mid_left_leg,
                'back': back_left_leg
            },
            'right': {
                'front': front_right_leg,
                'mid': mid_right_leg,
                'back': back_right_leg
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

    def get_readings(self):
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

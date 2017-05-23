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

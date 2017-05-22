class Stance(object):
    def __init__(self, front_left_point, mid_left_point, back_left_point, back_right_point, mid_right_point, front_right_point):
        self.points = {
            'left': {
                'front': front_left_point,
                'mid': mid_left_point,
                'back': back_left_point
            },
            'right': {
                'front': front_right_point,
                'mid': mid_right_point,
                'back': back_right_point
            }
        }

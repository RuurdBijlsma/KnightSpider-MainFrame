import point
from movement.stance import Stance
from point import Point3D


class DanceSequence(object):
    def __init__(self, start_storage=None):
        if start_storage is None:
            start_storage = []
        self.storage = start_storage

    def add_move(self, stance, time, servo_speed):
        self.storage.append((stance, time, servo_speed))
        return self

    def add_walk(self, f, time, servo_speed):
        self.storage.append((f, time, servo_speed))
        return self

    def concat_sequence(self, other_sequence):
        self.storage = self.storage + other_sequence.storage
        return self

    def __getitem__(self, item):
        return self.storage[item]

    def time(self):
        sum = 0
        for _, time, _ in self.storage:
            sum += time
        return sum

    def __len__(self):
        return len(self.storage)

BASE_GROUND_CLEARANCE = -40
STANDARD_SERVO_SPEED = 700

# Naming rules:
# Name must give some indication of the spider's pose
# Use underscores for spaces
# When defining a sequence of moves use a dash and then the index in the sequence
# Example: "wave-2"

POINT_WAVE_LEG_RAISED = Point3D(200, -10, 0)

STANCES = {
    "flat": Stance(
            front_left_point=point.OUT_OF_REACH,
            mid_left_point=point.OUT_OF_REACH,
            back_left_point=point.OUT_OF_REACH,
            front_right_point=point.OUT_OF_REACH,
            mid_right_point=point.OUT_OF_REACH,
            back_right_point=point.OUT_OF_REACH
    ),
    "stand": Stance(
            front_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            mid_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            back_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            front_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            mid_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            back_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0)
    ),
    "stand_low": Stance(
            front_left_point=Point3D(150, -30, 0),
            mid_left_point=Point3D(150, -30, 0),
            back_left_point=Point3D(150, -30, 0),
            front_right_point=Point3D(150, -30, 0),
            mid_right_point=Point3D(150, -30, 0),
            back_right_point=Point3D(150, -30, 0)
    ),
    "stand_high": Stance(
            front_left_point=Point3D(120, -100, 0),
            mid_left_point=Point3D(120, -100, 0),
            back_left_point=Point3D(120, -100, 0),
            front_right_point=Point3D(120, -100, 0),
            mid_right_point=Point3D(120, -100, 0),
            back_right_point=Point3D(120, -100, 0)
    ),
    "raise_mid_up": Stance(
            front_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            mid_left_point=Point3D(100, 150, 0),
            back_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            front_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            mid_right_point=Point3D(100, 150, 0),
            back_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0)
    ),
    "raise_mid_flat": Stance(
            front_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            mid_left_point=point.OUT_OF_REACH,
            back_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            front_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            mid_right_point=point.OUT_OF_REACH,
            back_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0)
    ),
    "upside_down": Stance(
            front_left_point=Point3D(100, -BASE_GROUND_CLEARANCE, 0),
            mid_left_point=Point3D(100, -BASE_GROUND_CLEARANCE, 0),
            back_left_point=Point3D(100, -BASE_GROUND_CLEARANCE, 0),
            front_right_point=Point3D(100, -BASE_GROUND_CLEARANCE, 0),
            mid_right_point=Point3D(100, -BASE_GROUND_CLEARANCE, 0),
            back_right_point=Point3D(100, -BASE_GROUND_CLEARANCE, 0)
    ),
    "upside_down_high": Stance(
            front_left_point=Point3D(100, 200, 0),
            mid_left_point=Point3D(100, 200, 0),
            back_left_point=Point3D(100, 200, 0),
            front_right_point=Point3D(100, 200, 0),
            mid_right_point=Point3D(100, 200, 0),
            back_right_point=Point3D(100, 200, 0)
    ),
    "dead": Stance(
            front_left_point=Point3D(80, 100, 0),
            mid_left_point=Point3D(80, 100, 0),
            back_left_point=Point3D(80, 100, 0),
            front_right_point=Point3D(80, 100, 0),
            mid_right_point=Point3D(80, 100, 0),
            back_right_point=Point3D(80, 100, 0)
    ),
    "pirouette-1": Stance(
            front_left_point=Point3D(70, -25, -100),
            mid_left_point=point.OUT_OF_REACH,
            back_left_point=point.OUT_OF_REACH,
            front_right_point=point.OUT_OF_REACH,
            mid_right_point=point.OUT_OF_REACH,
            back_right_point=Point3D(70, -25, 100)
    ),
    "pirouette-2": Stance(
            front_left_point=Point3D(70, -25, 100),
            mid_left_point=point.OUT_OF_REACH,
            back_left_point=point.OUT_OF_REACH,
            front_right_point=point.OUT_OF_REACH,
            mid_right_point=point.OUT_OF_REACH,
            back_right_point=Point3D(70, -25, -100)
    ),
    "leg_wave-1": Stance(
            front_left_point=POINT_WAVE_LEG_RAISED,
            mid_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            back_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            front_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            mid_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            back_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0)
    ),
    "leg_wave-2": Stance(
            front_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            mid_left_point=POINT_WAVE_LEG_RAISED,
            back_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            front_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            mid_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            back_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0)
    ),
    "leg_wave-3": Stance(
            front_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            mid_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            back_left_point=POINT_WAVE_LEG_RAISED,
            front_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            mid_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            back_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0)
    ),
    "leg_wave-4": Stance(
            front_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            mid_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            back_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            front_right_point=POINT_WAVE_LEG_RAISED,
            mid_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            back_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0)
    ),
    "leg_wave-5": Stance(
            front_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            mid_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            back_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            front_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            mid_right_point=POINT_WAVE_LEG_RAISED,
            back_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0)
    ),
    "leg_wave-6": Stance(
            front_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            mid_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            back_left_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            front_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            mid_right_point=Point3D(100, BASE_GROUND_CLEARANCE, 0),
            back_right_point=POINT_WAVE_LEG_RAISED
    ),
    "body_wave-1": Stance(
            front_left_point=Point3D(100, BASE_GROUND_CLEARANCE + 30, 0),
            mid_left_point=Point3D(100, BASE_GROUND_CLEARANCE + 30, 0),
            back_left_point=Point3D(100, BASE_GROUND_CLEARANCE + 30, 0),
            front_right_point=Point3D(100, BASE_GROUND_CLEARANCE - 30, 0),
            mid_right_point=Point3D(100, BASE_GROUND_CLEARANCE - 30, 0),
            back_right_point=Point3D(100, BASE_GROUND_CLEARANCE - 30, 0)
    ),
    "body_wave-2": Stance(
            front_left_point=Point3D(100, BASE_GROUND_CLEARANCE - 30, 0),
            mid_left_point=Point3D(100, BASE_GROUND_CLEARANCE - 30, 0),
            back_left_point=Point3D(100, BASE_GROUND_CLEARANCE - 30, 0),
            front_right_point=Point3D(100, BASE_GROUND_CLEARANCE + 30, 0),
            mid_right_point=Point3D(100, BASE_GROUND_CLEARANCE + 30, 0),
            back_right_point=Point3D(100, BASE_GROUND_CLEARANCE + 30, 0)
    ),
}

WAVE_DELAY = 0.2
WAVE_SERVO_SPEED = 1000
LEG_WAVE = DanceSequence([
    (STANCES["leg_wave-1"], WAVE_DELAY, WAVE_SERVO_SPEED),
    (STANCES["leg_wave-2"], WAVE_DELAY, WAVE_SERVO_SPEED),
    (STANCES["leg_wave-3"], WAVE_DELAY, WAVE_SERVO_SPEED),
    (STANCES["leg_wave-4"], WAVE_DELAY, WAVE_SERVO_SPEED),
    (STANCES["leg_wave-5"], WAVE_DELAY, WAVE_SERVO_SPEED),
    (STANCES["leg_wave-6"], WAVE_DELAY, WAVE_SERVO_SPEED),
])

BODY_WAVE = DanceSequence([
    (STANCES["body_wave-1"], WAVE_DELAY, STANDARD_SERVO_SPEED),
    (STANCES["stand"], WAVE_DELAY, STANDARD_SERVO_SPEED),
    (STANCES["body_wave-2"], WAVE_DELAY, STANDARD_SERVO_SPEED),
    (STANCES["stand"], WAVE_DELAY, STANDARD_SERVO_SPEED),
    (STANCES["body_wave-1"], WAVE_DELAY, STANDARD_SERVO_SPEED),

])

LAY_DOWN_GENTLY = DanceSequence([
    (STANCES["stand_low"], 0.7, 200),
    (STANCES["flat"], 0.7, 200)
])

SAYONARA_MAXWELL_BPM = 62
SAYONARA_MAXWELL_DELAY = SAYONARA_MAXWELL_BPM / 60

CHEER_BPM_DIVIDER = 4

CHEER = DanceSequence([
    (STANCES["stand"], SAYONARA_MAXWELL_DELAY / CHEER_BPM_DIVIDER, 1000),
    (STANCES["raise_mid_up"], SAYONARA_MAXWELL_DELAY / CHEER_BPM_DIVIDER, 1000),
    (STANCES["raise_mid_flat"], SAYONARA_MAXWELL_DELAY / CHEER_BPM_DIVIDER, 1000),
    (STANCES["raise_mid_up"], SAYONARA_MAXWELL_DELAY / CHEER_BPM_DIVIDER, 1000),
    (STANCES["raise_mid_flat"], SAYONARA_MAXWELL_DELAY / CHEER_BPM_DIVIDER, 1000),
    (STANCES["raise_mid_up"], SAYONARA_MAXWELL_DELAY / CHEER_BPM_DIVIDER, 1000),
    (STANCES["raise_mid_flat"], SAYONARA_MAXWELL_DELAY / CHEER_BPM_DIVIDER, 1000),
    (STANCES["raise_mid_up"], SAYONARA_MAXWELL_DELAY / CHEER_BPM_DIVIDER, 1000),
    (STANCES["raise_mid_flat"], SAYONARA_MAXWELL_DELAY / CHEER_BPM_DIVIDER, 1000),
    (STANCES["raise_mid_up"], SAYONARA_MAXWELL_DELAY / CHEER_BPM_DIVIDER, 1000),
    (STANCES["raise_mid_flat"], SAYONARA_MAXWELL_DELAY / CHEER_BPM_DIVIDER, 1000),
    (STANCES["raise_mid_up"], SAYONARA_MAXWELL_DELAY / CHEER_BPM_DIVIDER, 1000),
    (STANCES["raise_mid_flat"], SAYONARA_MAXWELL_DELAY / CHEER_BPM_DIVIDER, 1000),
    (STANCES["stand"], SAYONARA_MAXWELL_DELAY / CHEER_BPM_DIVIDER, 1000),
])

def create_sayora_maxwell_dance(spider):
    sequence = DanceSequence()

    # DO NOT RUN, KILLS PLASTIC

    # sequence\
    #     .concat_sequence(LEG_WAVE_SEQUENCE)\
    #     .concat_sequence(LEG_WAVE_SEQUENCE)\
    #     .add_move(STANCES["stand_high"], SAYONARA_MAXWELL_DELAY, STANDARD_SERVO_SPEED)\
    # .add_walk(spider.turn_left, 6.35, 1000)\
    sequence\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\
        .add_move(STANCES["stand"], 0.4, 1000)\
        .add_move(STANCES["flat"], 0.4, 1000)\

        # .add_move(STANCES["stand"], 0.5, 450)\
        # .concat_sequence(CHEER)\
        # .add_move(STANCES["stand"], 0.2, 1000) \
        # .concat_sequence(BODY_WAVE)\
        # .add_move(STANCES["stand"], 0.2, 1000) \
        # .add_walk(spider.turn_left, 5.5, 1000) \
        # .add_move(STANCES["stand"], 0.2, 1000) \
        # .concat_sequence(LEG_WAVE)\
        # .concat_sequence(LEG_WAVE)\
        # .add_move(STANCES["stand"], 0.2, 1000) \
        # .concat_sequence(LAY_DOWN_GENTLY)\
        # .add_move(STANCES["dead"], SAYONARA_MAXWELL_DELAY, STANDARD_SERVO_SPEED)\

    print("Dance length", sequence.time())

    return sequence
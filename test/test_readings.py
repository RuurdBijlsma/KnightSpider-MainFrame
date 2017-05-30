from leg import Leg
from readings_worker import ReadingUpdater
from spider import Spider

legs = [
    Leg(30, 11, 12, 13),
    Leg(0, 21, 22, 23),
    Leg(-30, 31, 32, 33),
    Leg(30, 41, 42, 43),
    Leg(-30, 31, 32, 33),
    Leg(30, 41, 42, 43),
]

spider = Spider(
    front_right_leg=legs[0],
    mid_right_leg=legs[1],
    back_right_leg=legs[2],
    front_left_leg=legs[3],
    mid_left_leg=legs[4],
    back_left_leg=legs[5],
)

background_thread = ReadingUpdater(frequency=2, spider=spider)
background_thread.start()

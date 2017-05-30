from leg import Leg
from readings_worker import ReadingUpdater
from spider import Spider

legs = [
    Leg(leg_id=1, angle=-30),
    Leg(leg_id=2, angle=0),
    Leg(leg_id=3, angle=30),
    Leg(leg_id=4, angle=-30),
    Leg(leg_id=5, angle=0),
    Leg(leg_id=6, angle=30),
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

print("blokt nniet")

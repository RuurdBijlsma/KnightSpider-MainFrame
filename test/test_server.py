import ax12_serial
from leg import Leg
from readings_worker import ReadingsWorker
from spider import Spider
from socket_listener.server import SocketServer

legs = [
    Leg(leg_id=1, angle=-30),
    Leg(leg_id=2, angle=0),
    Leg(leg_id=3, angle=30),
    Leg(leg_id=4, angle=-30),
    Leg(leg_id=5, angle=0),
    Leg(leg_id=6, angle=30),
]

# angle = 60

spider = Spider(front_left_leg=legs[0],
                mid_left_leg=legs[1],
                back_left_leg=legs[2],
                front_right_leg=legs[3],
                mid_right_leg=legs[4],
                back_right_leg=legs[5])

ax12_serial.init()
ReadingsWorker(frequency=5, spider=spider).start()


SocketServer()

while True:
    pass
from periodic_worker import PeriodicWorker
from socket_listener import identifiers
from socket_listener.message import Message


class DataBroadcaster(PeriodicWorker):
    def __init__(self, spider, server, frequency):
        self.server = server
        self.spider = spider
        super().__init__(frequency)

    def update(self):
        self.server.broadcast(Message(
            identifiers.SPIDER,
            self.spider.get_info().to_json()
        ))

        # self.server.broadcast(Message(
        #     identifiers.ANGLES,
        #     self.spider.get_servo_angles_json()
        # ))

        self.server.broadcast(Message(
            identifiers.SERVOS,
            self.spider.get_servo_readings_json()
        ))
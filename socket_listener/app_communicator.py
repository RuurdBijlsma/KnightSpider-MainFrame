from readings_worker import ReadingsWorker
from servo import Servo
from socket_listener import identifiers
from socket_listener.data_broadcaster import DataBroadcaster
from socket_listener.message import Message
from socket_listener.server import Server

class AppCommunicator(object):
    UPDATE_FREQUENCY = 5

    def __init__(self, spider):
        self.spider = spider
        self.server = Server()
        self.server.register_message_handler(identifiers.GET_SERVO, self.handle_servo_request)
        self.server.register_udp_callback(self.udp_callback)
        self.server.start_listen_thread()
        self.data_broadcaster = DataBroadcaster(spider, self.server, self.UPDATE_FREQUENCY).start()
        self.readings_worker = ReadingsWorker(frequency=5, spider=spider).start()

    def udp_callback(self, data):
        print("UDP:", data)
        self.spider.parse_controller_update(data)

    def handle_servo_request(self, connection, payload):
        print("getting readings for", payload)
        try:
            id = int(payload)
            servo_info = self.spider.get_servo_by_id(id).readings.to_json()
            print("got readings", servo_info)
            self.server.client_send_queue[connection].put(Message(identifiers.SERVO, servo_info))
        except ValueError:
            print("payload is not an id")
            pass

    def close(self):
        self.server.close()
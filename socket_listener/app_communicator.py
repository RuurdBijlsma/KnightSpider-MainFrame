from readings_worker import ReadingsWorker
from socket_listener import identifiers
from socket_listener.data_broadcaster import DataBroadcaster
from socket_listener.message import Message
from socket_listener.server import Server


class AppCommunicator(object):
    UPDATE_FREQUENCY = 1
    CONTROLLER_UPDATE_INTERVAL = 0.15
    t_last = None

    def __init__(self, spider, broadcast=True):
        self.spider = spider
        self.server = Server(enable_udp=True)
        self.server.register_udp_callback(self.udp_callback)
        self.server.register_message_handler(identifiers.GET_SERVO, self.handle_servo_request)
        self.server.start_listen_thread()
        if (broadcast):
            self.data_broadcaster = DataBroadcaster(spider, self.server, self.UPDATE_FREQUENCY).start()
            self.readings_worker = ReadingsWorker(frequency=self.UPDATE_FREQUENCY, spider=spider).start()
        else:
            self.data_broadcaster = DataBroadcaster(spider, self.server, self.UPDATE_FREQUENCY, send_readings=False)

    mag = 0

    def udp_callback(self, data):
        print("UDP", data)
        # if self.t_last is None or self.t_last + self.CONTROLLER_UPDATE_INTERVAL < time.time():
        #     self.t_last = time.time()
        #     self.spider.parse_controller_update(data)
        #
        self.mag += 1
        if self.mag % 10 == 0:
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

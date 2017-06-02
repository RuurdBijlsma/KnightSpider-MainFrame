from socket_listener.data_broadcaster import DataBroadcaster
from socket_listener.server import Server

class AppCommunicator(object):
    UPDATE_FREQUENCY = 2

    def __init__(self, spider):
        self.spider = spider
        self.server = Server()
        self.server.start_listen_thread()
        self.data_broadcaster = DataBroadcaster(spider, self.server, self.UPDATE_FREQUENCY).start()

    def close(self):
        self.server.close()
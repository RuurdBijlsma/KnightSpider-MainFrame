import socket
import signal
import sys
import threading
from queue import Queue

import fcntl

import time


class Server(object):
    HOST = ''  # Symbolic name meaning all available interfaces
    PORT = 4980  # Arbitrary non-privileged port
    RECV_SIZE = 1024

    def __init__(self, host=HOST, port=PORT):
        self.connections = []
        self.client_send_queue = {}
        self.cancel_listening = False

        self.client_threads = []

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')

        # Bind socket to local host and port
        try:
            self.socket.bind((host, port))
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        signal.signal(signal.SIGINT, self.sigint_handler)

        print('Socket bound at {}:{}'.format(self.socket.getsockname()[0], self.PORT))

        # Start listening on socket
        self.socket.setblocking(True)
        self.socket.settimeout(1)
        self.socket.listen(10)
        print('Socket now listening')

    def start_listen_thread(self):
        self.listen_thread = threading.Thread(target=self.listen_loop)
        self.listen_thread.start()

    def listen_loop(self):
        try:
            while not self.cancel_listening:
                try:
                    connection, address = self.socket.accept()
                    connection.setblocking(True)
                    connection.settimeout(1) # Block for 1 second before thorwing a timeout exception

                    connection.send(self.prepare_for_sending("henlo frend").encode())

                    print('Connected with ' + address[0] + ':' + str(address[1]))
                    self.connections.append(connection)
                    self.client_send_queue[connection] = Queue()

                    client_thread = threading.Thread(target=self.client_loop, args=[connection])
                    client_thread.start()
                    self.client_threads.append(client_thread)
                except socket.timeout:
                    pass
        except Exception as e:
            print(e)
        finally:
            print("Lost socket connection")
            self.close()

    def client_loop(self, connection):
        try:
            while not self.cancel_listening:
                queue = self.client_send_queue[connection]

                while not queue.empty():
                    data = self.prepare_for_sending(queue.get())
                    connection.send(data.encode())

                try:
                    self.handle_message(connection, connection.recv(self.RECV_SIZE).decode("utf-8"))
                except socket.timeout:
                    pass
        finally:
            print("Lost connection to client")
            self.connections.remove(connection)
            try:
                connection.close()
            except:
                pass
            self.client_threads.remove(threading.current_thread())

    def prepare_for_sending(self, data):
        if not isinstance(data, str):
            data = str(data)

        if data[-1:] != '\n':
            data += '\n'
        return data

    def handle_message(self, connection, message):
        print("received", message)
        self.broadcast("response " + message)

    def broadcast(self, data):
        print("broadcast", data)
        for connection in self.connections:
            self.client_send_queue[connection].put(data)

    def sigint_handler(self, signal, frame):
        print("Received SIGINT, cleaning up socket")
        self.close()
        sys.exit(0)

    def close(self):
        self.cancel_listening = True
        time.sleep(1)
        for connection in self.connections:
            connection.close()
        self.socket.close()
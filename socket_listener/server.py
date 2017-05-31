import socket
import struct
import sys
import _thread

import fcntl


class SocketServer(object):
    def __init__(self):
        HOST = '0.0.0.0'  # Symbolic name meaning all available interfaces
        PORT = 4980  # Arbitrary non-privileged port

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')

        # Bind socket to local host and port
        try:
            s.bind((HOST, PORT))
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        print('Socket bound at {}:{}'.format(s.getsockname()[0], PORT))

        # Start listening on socket
        s.listen(10)
        print('Socket now listening')


def get_servo_info():
    return "dit komt in de battery\n"


# # Function for handling connections. This will be used to create threads
# def client_thread(conn):
#     # Sending message to connected client
#     conn.send(('Welcome to the server.\n').encode())  # send only takes string
#
#     # infinite loop so that function do not terminate and thread do not end.
#     while True:
#
#         print('Now waiting for android')
#         # Receiving from client
#         data = conn.recv(1024)
#
#         incoming = data.decode('utf-8')
#         outgoing = {
#             "servo": get_servo_info()
#         }[incoming]
#         print("Got response: " + incoming)
#         print("Replying: ", outgoing)
#
#         if not data:
#             break
#         conn.send(outgoing.encode())
#         print('Reply sent')
#
#     # came out of loop
#     conn.close()
#
#
# # now keep talking with the client
# while 1:
#     # wait to accept a connection - blocking call
#     connection, address = s.accept()
#     print('Connected with ' + address[0] + ':' + str(address[1]))
#
#     # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
#     _thread.start_new_thread(client_thread, (connection,))
#
# s.close()

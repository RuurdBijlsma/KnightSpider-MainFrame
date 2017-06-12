import socket


def send(data, port=4980, addr='141.252.240.35'):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((addr, port))
    s.send(data)


while True:
    msg = input()
    # send((msg + '\n').encode())
    print(msg)

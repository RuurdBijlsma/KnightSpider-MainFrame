import ax12_serial
from leg import Leg
from readings_worker import ReadingsWorker
from socket_listener.app_communicator import AppCommunicator
from spider import Spider

ax12_serial.init()

spider = Spider()

ReadingsWorker(frequency=5, spider=spider).start()


app = AppCommunicator(spider)

print("press q to terminate")
while True:
    val = input()
    if val == 'q':
        break
    elif val == 's':
        app.server.broadcast("hey")

app.close()
print("Terminated")
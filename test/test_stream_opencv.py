from threading import Thread

import cv2
import numpy as np
import io

import time

import pistreaming.server

server = pistreaming.server.Server()
t = Thread(target=server.start)
t.start()
time.sleep(1)

# array = server.stream

# im = cv2.imdecode(array, cv2.IMREAD_ANYCOLOR)

cv2.imwrite("sok.jpeg", server.get_capture())

server.close()

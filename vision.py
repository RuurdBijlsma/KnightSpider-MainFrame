import cv2
import pistreaming.server
from threading import Thread
import vision.shapes as shapes
import vision.road_detector as road_detector
import time


class Vision:
    def __init__(self):
        self.server = pistreaming.server.Server()
        t = Thread(target=self.server.start)
        t.start()
        time.sleep(1)

        # self.frame = server.get_capture()

    def find_heart(self):
        shapes.find_shape(self.server.get_capture(), cv2.imwrite("images/hart2.jpg", 0))

    def find_diamond(self):
        shapes.find_shape(self.server.get_capture(), cv2.imwrite("images/ruiten.png", 0))

    def find_spades(self):
        shapes.find_shape(self.server.get_capture(), cv2.imwrite("images/spade.jpg", 0))

    def find_club(self):
        shapes.find_shape(self.server.get_capture(), cv2.imwrite("images/club.jpg", 0))

    def find_road(self):


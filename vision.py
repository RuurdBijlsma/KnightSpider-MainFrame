import cv2
import pistreaming.server
from threading import Thread
import vision.shapes as shapes
import vision.road_detector as road_detector
import time
import vision.eggs as eggs


class Vision:
    def __init__(self):
        self.server = pistreaming.server.Server()
        t = Thread(target=self.server.start)
        t.start()
        time.sleep(1)

    def find_heart(self):
        return shapes.find_shape(self.server.get_capture(), cv2.imwrite("images/hart2.jpg", 0))

    def find_diamond(self):
        return shapes.find_shape(self.server.get_capture(), cv2.imwrite("images/ruiten.png", 0))

    def find_spades(self):
        return shapes.find_shape(self.server.get_capture(), cv2.imwrite("images/spade.jpg", 0))

    def find_club(self):
        return shapes.find_shape(self.server.get_capture(), cv2.imwrite("images/club.jpg", 0))

    def find_white_egg(self):
        return eggs.find_egg(self.server.get_capture(), cv2.imwrite("images/mainegg.png"), True, 50)

    def find_colored_egg(self):
        return eggs.find_egg(self.server.get_capture(), cv2.imwrite("images/mainegg.png"), False, 50)

    def find_road(self):
        return road_detector.find_road(self.server.get_capture())

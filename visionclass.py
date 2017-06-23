import cv2
import pistreaming.server
from threading import Thread
import vision.shapes as shapes
import vision.road_detector as road_detector
import time
import vision.eggs as eggs
from vision import magic


class Vision:
    IMAGE_FOLDER_PATH = "vision/images/"

    def __init__(self):
        print("Starting vision")
        self.server = pistreaming.server.Server()
        t = Thread(target=self.server.start)
        t.start()
        # todo make not stupid
        time.sleep(1)

    def find_heart(self):
        return shapes.find_shape(self.server.get_capture(), cv2.imread(self.IMAGE_FOLDER_PATH + "hart2.jpg", 0))

    def find_diamond(self):
        return shapes.find_shape(self.server.get_capture(), cv2.imread(self.IMAGE_FOLDER_PATH + "ruiten.png", 0))

    def find_spades(self):
        return shapes.find_shape(self.server.get_capture(), cv2.imread(self.IMAGE_FOLDER_PATH + "spade.jpg", 0))

    def find_club(self):
        return shapes.find_shape(self.server.get_capture(), cv2.imread(self.IMAGE_FOLDER_PATH + "club.jpg", 0))

    def find_white_egg(self):
        return eggs.find_egg(self.server.get_capture(), cv2.imread(self.IMAGE_FOLDER_PATH + "mainegg.png", 0), True, 50)

    def find_colored_egg(self):
        return eggs.find_egg(self.server.get_capture(), cv2.imread(self.IMAGE_FOLDER_PATH + "mainegg.png", 0), False, 50)

    def find_road(self):
        return road_detector.find_road(self.server.get_capture())

    def close(self):
        self.server.close()





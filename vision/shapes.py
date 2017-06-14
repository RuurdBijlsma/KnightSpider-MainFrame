import cv2
import numpy as np
import time
from shape_detector import ShapeDetector
import sys
from threading import Thread
# import pistreaming.server as server

# cap = None
# shape = None
# print(sys.argv[0])
# targetImg = cv2.imread('images/club.jpg',0)
#
#
# if shape == "diamond":
#     targetImg = cv2.imread('images/ruiten.png',0)
# elif shape == "club":
#     targetImg = cv2.imread('images/club.jpg',0)
# elif shape == "spade":
#     targetImg = cv2.imread('images/spade.jpg',0)
# elif shape == "heart":
#     targetImg = cv2.imread('images/hart2.jpg',0)
#
#
MIN_AREA = 5
MAX_SIMILARITY_VALUE = 0.1


def find_shape(frame, target_img):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    shape_detector = ShapeDetector(target_img, contour_index=None)
    contours, found_match, match_contour, similarity = shape_detector.detect(frame,MIN_AREA)

    if found_match == "success":
        frame = cv2.drawContours(frame, match_contour, -1, (255,0,0),3)

    cv2.imshow('result', frame)

cv2.destroyAllWindows()

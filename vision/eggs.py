import cv2
import numpy as np

from vision import magic
from vision.shape_detector import ShapeDetector

def find_egg(frame, targetImg, white, MIN_AREA):
    lower = (0, 15, 80)
    upper = (50, 255, 255)
    if white:
        lower = (0, 0, 200)
        upper = (180, 80, 255)
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    shape_detector = ShapeDetector(targetImg)
    contours, found_match, match_contour, similarity = shape_detector.detectEgg(res, MIN_AREA, 0.2)

    if found_match == "success":
        return shape_detector.on_screen(frame, match_contour)
    else:
        print("not found")
        return magic.DEFAULT_SIDE

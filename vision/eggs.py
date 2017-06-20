import cv2
import numpy as np
from vision.shape_detector import ShapeDetector
import vision.magic


def find_egg(frame, targetImg, white, MIN_AREA):
    lower = (0, 15, 80)
    upper = (20, 209, 2550)
    if white:
        lower = (0, 0, 200)
        upper = (180, 80, 255)
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    shape_detect = ShapeDetector(targetImg, contour_index=None)
    contours, found_match, match_contour, similarity = shape_detect.detectEgg(res, MIN_AREA, 0.2)

    if found_match == "success":
        if ShapeDetector.is_centered(frame, match_contour) is False:
            return ShapeDetector.on_screen(frame, match_contour)
        elif ShapeDetector.is_centered(frame, match_contour):
            return magic.CENTER
    else:
        return magic.DEFAULT_SIDE
import cv2
import numpy as np
import time
from shape_detector import ShapeDetector
import sys
from threading import Thread
import magic

MIN_AREA = 5
MAX_SIMILARITY_VALUE = 0.1

def find_shape(frame, target_img):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    shape_detector = ShapeDetector(target_img, contour_index=None)
    contours, found_match, match_contour, similarity = shape_detector.detect(frame,MIN_AREA)

    if found_match == "success":
        if ShapeDetector.is_centered(frame, match_contour) is False:
            return ShapeDetector.on_screen(frame,match_contour)
        elif ShapeDetector.is_centered(frame, match_contour):
            return CENTER
    else:
        return magic.DEFAULT_SIDE


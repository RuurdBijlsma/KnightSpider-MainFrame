import cv2
from vision.shape_detector import ShapeDetector
import vision.magic
from vision import magic

MIN_AREA = 5
MAX_SIMILARITY_VALUE = 0.1


def find_shape(frame, target_img):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    shape_detector = ShapeDetector(target_img)
    contours, found_match, match_contour, similarity = shape_detector.detect(frame, MIN_AREA)

    if found_match == "success":
        return shape_detector.on_screen(frame, match_contour)
    else:
        print("not found")
        return magic.DEFAULT_SIDE


    #     if shape_detector.is_centered(frame, match_contour) is False:
    #         return shape_detector.on_screen(frame, match_contour)
    #     elif shape_detector.is_centered(frame, match_contour):
    #         return magic.CENTER
    # else:
    #     return magic.DEFAULT_SIDE


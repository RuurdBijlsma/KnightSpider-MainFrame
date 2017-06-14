import cv2
import numpy as np
from shape_detector import ShapeDetector

def find_egg(frame, white, MIN_AREA):
    lower = (0,15,80)
    upper = (20,209,2550)
    if white:
        lower = (0,0,200)
        upper = (180,80,255)
    blurred = cv2.GaussianBlur(frame,(5,5), 0)
    hsv = cv2.GaussianBlur(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    shape_detect = ShapeDetector(targetImg, contour_index=None)
    contours, found_match, match_contour, similarity = shape_detect.detectEgg(res, MIN_AREA, 0.2)

    if found_match == "success":
        M = cv2.moments(match_contour)
        if M['m00'] > 1000:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            frame = cv2.drawContours(frame, match_contour,-1,(255,0,0),3)
            frame = cv2.circle(frame,(cx,cy), 3, (255,0,0), 3)


    cv2.imshow("result", frame)

cv2.destroyAllWindows()

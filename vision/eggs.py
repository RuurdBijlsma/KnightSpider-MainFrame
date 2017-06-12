import cv2
import numpy as np
from shape_detector import ShapeDetector


cap = cv2.VideoCapture(0)

targetImg = cv2.imread('images/eggContour.jpg',0)

shape_detect = ShapeDetector(targetImg, contour_index=None)

MIN_AREA = 50

while 1:
    _, frame = cap.read()
    #frame = cv2.GaussianBlur(frame,(5,5), 0)
    canny = cv2.Canny(frame,55,150)

    contours, found_match, match_contour, similarity = shape_detect.detectEgg(frame, MIN_AREA)

    if found_match == "success":
        M = cv2.moments(match_contour)
        if M['m00'] > 1000:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            frame = cv2.drawContours(frame, match_contour,-1,(255,0,0),3)
            frame = cv2.circle(frame,(cx,cy), 3, (255,0,0), 3)


    cv2.imshow("output", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import cv2
import numpy as np
from shape_detector import ShapeDetector
import sys

print(sys.argv[0])
targetImg = cv2.imread('images/club.jpg',0)

if sys.argv[1] == "diamond":
    targetImg = cv2.imread('images/ruiten.png',0)
    print("diamond selected")
elif sys.argv[1] == "club":
    targetImg = cv2.imread('images/club.jpg',0)
    print("club selected")
elif sys.argv[1] == "spade":
    targetImg = cv2.imread('images/spade.jpg',0)
    print("spade selected")
else:
    targetImg = cv2.imread('images/hart2.jpg',0)
    print("hart selected")


#targetImg = cv2.imread('images/club.jpg',0)
#targetImg = cv2.imread('images/spade.jpg',0)
#targetImg = cv2.imread('images/ruiten.png',0)

#img2 = cv2.imread('23.jpg',0)

cap = cv2.VideoCapture(0)


#_, thresh = cv2.threshold(targetImg, 127, 255,0)
#_,contours,_ = cv2.findContours(thresh,2,1)
#cnt1 = contours[1]

MIN_AREA = 5
MAX_SIMILARITY_VALUE = 0.1

shape_detector = ShapeDetector(targetImg, contour_index=None)

while 1:
    grabbed, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    contours, found_match, match_contour, similarity = shape_detector.detect(frame,MIN_AREA)

    if found_match == "success":
        frame = cv2.drawContours(frame, match_contour, -1, (255,0,0),3)
    
    
    cv2.imshow('result', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

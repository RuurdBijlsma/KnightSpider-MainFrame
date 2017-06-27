import numpy as np
import cv2
import math

cap = cv2.VideoCapture(0)
upper = (17, 255, 255)
lower = (0, 100, 100)


while 1:
    _, img = cap.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(img, img, mask=blueMask)

    cv2.imshow("red?", res)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.realse()
cv2.destroyAllWindows()


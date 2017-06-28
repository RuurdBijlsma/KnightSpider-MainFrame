import numpy as np
import cv2
import math

cap = cv2.VideoCapture(0)
upper = (10, 255, 255)
lower = (0, 100, 100)

#lower = (120,10,10)
#upper = (255,90,90)


while 1:
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow("red?", res)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()


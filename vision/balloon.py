from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time

start_time = time.time()


redLower = (0,100,100)
redUpper = (3,255,255)

blackLower = (0,0,0)
blackUpper = (60,60,60)

camera = cv2.VideoCapture(0)

while True:
    
    (grabbed, frame) = camera.read()

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    redMask = cv2.inRange(hsv, redLower, redUpper)
    redMask = cv2.erode(redMask, None, iterations=2)
    redMask = cv2.dilate(redMask, None, iterations=2)

    cnts = cv2.findContours(redMask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    

    res = frame
    
    if len(cnts) > 0:
            for c in cnts:
                M = cv2.moments(c)
                if(M['m00'] > 1000):
                    hull = cv2.convexHull(c)
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    res = cv2.drawContours(res,[hull],-1,(0,255,255),3)
                    res = cv2.circle(res,(cx,cy),3,(0,255,255),3)
                   
    cv2.imshow("Frame", res)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        print("%s seconds" % (time.time() - start_time))
        break

camera.release()
cv2.destroyAllWindows()

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('images/frank.jpg')
img = cv2.medianBlur(img,5)

lower = (0,30,90)
upper = (50,255,255)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv,lower,upper)
mask = cv2.erode(mask,None,iterations=2)
mask = cv2.dilate(mask, None, iterations=2)

img = cv2.imread('images/frank.jpg', 0)
img = cv2.medianBlur(img,9)

_,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11,2)
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

titles = ["normal", "mean", "gaussian","mask"]
images = [th1,th2,th3,mask]

for i in range(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])
plt.show()
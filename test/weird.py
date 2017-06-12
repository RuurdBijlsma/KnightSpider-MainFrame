import cv2
import time

frames = [cv2.imread("im1.jpg"),
          cv2.imread("im2.jpg")]

cv2.namedWindow("image")
cv2.createTrackbar('bpm', 'image', 200, 400, lambda x: None)

index = 0
while (True):
    speed = cv2.getTrackbarPos('bpm', 'image')
    speed = float(60 / speed)

    cv2.imshow("image", frames[index])
    index += 1
    if (index > 1):
        index = 0
    time.sleep(speed)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

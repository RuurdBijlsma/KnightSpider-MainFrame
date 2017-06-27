import cv2
import numpy as np

from vision import magic

resolution = 500

# capture = cv2.VideoCapture(0)
# capture.set(3, resolution / 9 * 16)
# capture.set(4, resolution)
#
# cv2.namedWindow('image')
# cv2.createTrackbar('low', 'image', 110, 255, lambda x: None)
# cv2.createTrackbar('high', 'image', 131, 255, lambda x: None)
# cv2.createTrackbar('a', 'image', 150, 255, lambda x: None)

UPPER = (30, 255, 255)
LOWER = (0, 60, 60)


# def midpoint(p1, p2):
#     return (int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2))


def line_intersection(line1, line2):
    x_diff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    y_diff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])  # Typo was here

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(x_diff, y_diff)
    if div == 0:
        return False

    d = (det(*line1), det(*line2))
    x = det(d, x_diff) / div
    y = det(d, y_diff) / div
    return x, y


def find_road(frame):
    # ret, frame = capture.read()
    # frame = cv2.flip(frame, 0)

    # low = cv2.getTrackbarPos('low', 'image')
    # high = cv2.getTrackbarPos('high', 'image')
    # a = cv2.getTrackbarPos('a', 'image')

    low = 110
    high = 131
    a = 150

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, low, high)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, a)

    if lines is not None:
        road_lines = []
        angles = []

        print("Road lines count: ", len(lines))
        for line in lines:
            for rho, theta in line:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))

                from_pos = (x1, y1)
                to_pos = (x2, y2)

                angle = np.math.atan2(from_pos[1] - to_pos[1], from_pos[0] - to_pos[0])
                angle = np.math.degrees(angle)
                angle = angle + 180 if angle < 0 else angle
                if 40 < int(angle) < 85 or 120 < int(angle) < 175:
                    stop = False
                    for road_angle in angles:
                        if road_angle > 90 and angle > 90:
                            stop = True

                    if not stop:
                        # cv2.line(frame, from_pos, to_pos, (0, 0, 255), 2)
                        # cv2.putText(frame, str(angle), to_pos, cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0))
                        road_lines.append((from_pos, to_pos))
                        angles.append(angle)

        if len(road_lines) > 1:
            intersect = False
            index = 0
            while (True):
                intersect = line_intersection(road_lines[index], road_lines[index + 1])
                index += 1
                if (intersect):
                    break

            if intersect:
                # cv2.circle(frame, (int(intersect[0]), int(intersect[1])), 3, (0, 255, 0))

                height, width, channels = frame.shape
                mid = (width / 2, height / 2)
                offset = np.subtract(mid, intersect)
                # cv2.circle(frame, (int(mid[0]), int(intersect[1])), 3, (255, 0, 255))

                centre_offset = 100
                print("Found something, offset %s" % offset)
                return magic.RIGHT if offset[0] < -centre_offset else magic.LEFT if offset[
                                                                                        0] > centre_offset else magic.CENTER

    print("Found nothing")
    return magic.CENTER


def is_circle_on_screen(frame):
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    redMask = cv2.inRange(hsv, LOWER, UPPER)
    _, thresh = cv2.threshold(redMask, 127, 255, 0)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        # if (area > 0):
        #     print("Cunt area:", area)
        if area > 2000:
            return True

    return False

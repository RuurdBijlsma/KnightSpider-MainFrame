import cv2

from shape_detector import ShapeDetector

resolution = 500

capture = cv2.VideoCapture(0)
capture.set(3, resolution / 9 * 16)
capture.set(4, resolution)


def nothing(x): pass


cv2.namedWindow('image')
cv2.createTrackbar('T1', 'image', 300, 300, nothing)
cv2.createTrackbar('T2', 'image', 220, 300, nothing)

threshold1 = cv2.getTrackbarPos('T1', 'image')
threshold2 = cv2.getTrackbarPos('T2', 'image')

target_shape = cv2.imread('images/hart.jpg', 1)
shape_detector = ShapeDetector(target_shape, contour_index=1)

while True:
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)

    threshold1 = cv2.getTrackbarPos('T1', 'image')
    threshold2 = cv2.getTrackbarPos('T2', 'image')
    contours, found_match, match_contour, similarity, area = shape_detector.detect(frame,
                                                                                   min_threshold=threshold1,
                                                                                   max_threshold=threshold2,
                                                                                   min_area=500,
                                                                                   max_similarity_value=0.15)
    print("Found match" if found_match == "success" else "Did not found match", "Similarity:", similarity, "Area:",
          area)

    [cv2.drawContours(frame, [contour], 0, (0, 0, 255), 3) for contour in contours]
    if found_match == "success":
        cv2.drawContours(frame, [match_contour], 0, (0, 255, 0), 3)
    elif found_match == "similarityfail":
        cv2.drawContours(frame, [match_contour], 0, (255, 0, 0), 3)

    cv2.imshow('image', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()

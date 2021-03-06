import cv2
from vision import magic


class ShapeDetector(object):
    def __init__(self, shape, shape_min_threshold=127, contour_index=1):
        self.shape = shape
        _, self.thresh = cv2.threshold(shape, shape_min_threshold, 255, 0)

        _, shape_contours, _ = cv2.findContours(self.thresh, cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE)
        if contour_index is None:
            Exception("Shape not found in image, try adjusting thresholds")

        self.shape_contour = shape_contours[contour_index]

    def detect(self, image, min_area=400, max_similarity_value=0.1, min_thresh = 127,
               max_thresh = 255):

        _, thresh = cv2.threshold(image, min_thresh, max_thresh, 0)
        _, contours, _ = cv2.findContours(thresh,2,1)

        best_contour = contours[0]
        best_value = float('inf')
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > min_area:
                similarity = cv2.matchShapes(self.shape_contour, contour, 1, 0.0)
                if similarity < best_value:
                    best_contour = contour
                    best_value = similarity

        found_match = "areafail"
        if best_value > max_similarity_value and best_value is not float('inf'):
            found_match = "similarityfail"
        else:
            found_match = "success"

        return contours, found_match, best_contour, best_value

    def detectEgg(self, image, min_area=400, max_similarity_value=0.1, min_threshold=220, max_threshold=300):
        #image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        #image = cv2.medianBlur(image,5)
        thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        #edges = cv2.Canny(image, min_threshold, max_threshold, apertureSize=3)
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        best_contour = contours[0]
        best_value = float('inf')
        match_area = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > min_area:
                similarity = cv2.matchShapes(self.shape_contour, contour, 1, 0.0)
                if similarity < best_value:
                    best_contour = contour
                    best_value = similarity
                    match_area = area

        found_match = "areafail"

        if best_value > max_similarity_value and best_value is not float('inf'):
            found_match = "similarityfail"
        else:
            found_match = "success"

        return contours, found_match, best_contour, best_value

    # def is_centered(self, image, contour):
    #     height, width = image.shape
    #     mid = width / 2
    #
    #     M = cv2.moments(contour)
    #     if M['m00'] > 1000:
    #         cx = int(M['m10'] / M['m00'])
    #         if (mid - 10) < cx < (mid + 10):
    #             return True
    #
    #     return False

    CENTER_SIZE = 210

    def on_screen(self, image, contour):
        height, width, *_ = image.shape
        mid = width / 2

        M = cv2.moments(contour)
        if M['m00'] > 1000:
            print("m goed", M['m00'])
            cx = float(M['m10'] / M['m00'])
            if cx < (mid - self.CENTER_SIZE):
                print("Should go right")
                return magic.RIGHT
            elif cx > (mid + self.CENTER_SIZE):
                print("Should go left")
                return magic.LEFT
            else:
                print("Shape is centered")
                return magic.CENTER

        print("kut m", M['m00'])
        return magic.DEFAULT_SIDE



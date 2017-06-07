import cv2


class ShapeDetector(object):
    def __init__(self, shape, shape_min_threshold=180, contour_index=None):
        self.shape = shape
        _, self.thresh = cv2.threshold(cv2.cvtColor(shape, cv2.COLOR_BGR2GRAY), shape_min_threshold, 255,
                                       cv2.THRESH_BINARY)
        # self.shape_edges = cv2.Canny(shape, shape_min_threshold, shape_max_threshold, apertureSize=3)
        _, shape_contours, _ = cv2.findContours(self.thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contour_index is None:
            for index, contour in enumerate(shape_contours):
                shape_copy = self.shape.copy()
                cv2.drawContours(shape_copy, [contour], 0, (0, 180, 0), 3)
                cv2.imshow("Is this the correct contour? (Outlined in green)", shape_copy)
                k = cv2.waitKey(0)
                if k == 121:
                    contour_index = index
                    cv2.destroyWindow("Is this the correct contour? (Outlined in green)")
                    print("Contour index set to:", index)
                    break

        if contour_index is None:
            Exception("Shape not found in image, try adjusting thresholds")

        self.shape_contour = shape_contours[contour_index]

    def detect(self, image, min_area=400, max_similarity_value=0.1, min_threshold=220, max_threshold=300):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, min_threshold, max_threshold, apertureSize=3)
        _, contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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

        return contours, found_match, best_contour, best_value, match_area

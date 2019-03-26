#######################################################################################################################
# detector.py
#
# Responsible for most of the manipulation on the objects as well as the aruco detection
#
# Created by James Brock for Scott Hawley's Physics for AET class
#
# NOTE: SPECIFY ALL VARIABLES NEEDED IN THE VARIABLES.PY MODULE
#######################################################################################################################

import cv2
import cv2.aruco as aruco
import src.variables as variables
import numpy as np
import src.variables as v

parameters = aruco.DetectorParameters_create()

# lastReading = np.zeros((250,500,3), np.uint8)


class Detector:

    # lastReading = np.zeros((250, 500, 3), np.uint8)
    detected = False

    def __init__(self, name):
        self.name = name
        self.corners = None  # a np array of all corners detected from aruco markers
        self.ids = None  # a np array of the id numbers of the aruco markers
        self.final_corners = None  # the simplified 4 corners of the wanted box

    # Detects the aruco markers from a given image
    # Returns False if all four markers aren't found
    def detect_aruco_markers(self, img):
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.corners, self.ids, rejected = aruco.detectMarkers(grey, variables.markerDictionary, parameters=parameters)
        if self.ids is None or self.ids.size is not 4:
            return False
        self.get_marker_corners()

        return True

    # Draws the outlines of the aruco markers as well as a big box around the detected square for the final_corners
    # Takes an image and returns an image
    def draw_aruco_markers(self, img, big_outline=False):
        img = aruco.drawDetectedMarkers(img, self.corners)
        if big_outline:
            for i in range(4):
                img = cv2.line(img, self.final_corners[i], self.final_corners[(i + 1) % 4], (255, 0, 0), 3)
        return img

    # Takes an image and returns a warped version of it based on the final_corners
    def warp(self, img):
        src_pts = np.array(self.final_corners, dtype=np.float32)
        dst_pts = np.array([[0, 0], [500, 0], [500, 500], [0, 500]], dtype=np.float32)
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        return cv2.warpPerspective(img, M, (500, 500))

    # Takes in an image and creates a mask based on the threshold variables in the variables.py module
    def mask(self, img, threshold):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_color = np.array([v.color_low[v.get_number(self.name)], v.low_threshold[v.get_number(self.name)], v.low_threshold[v.get_number(self.name)]])
        upper_color = np.array([v.color_high[v.get_number(self.name)], 255, 255])
        mask = cv2.inRange(img, lower_color, upper_color)
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        return mask

    # Takes an image and returns a point tuple that represents the average distribution white in the image
    @classmethod
    def find_mask_point(cls, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        point = (0,0)
        points = []
        for i in range(500):  # relies on the image being 500x500 px
            for j in range(500):
                if img[i][j] > 250:
                    points.append((i,j))
        if len(points) == 0:
            return None
        points = np.array(points)
        point = np.mean(points, axis=0, dtype=int)
        point = (point[1],point[0])
        return point

    # Using the point of the reflective surface, it determines which zone on the surface is being reflected, based on
    # the previously saved point, and then saves the results in the variables.py module
    @classmethod
    def find_zone(cls):
        if v.point2 is not None:
            v.zone_x = int(v.point2[0]/(500/v.x_guide))
            v.zone_y = int(v.point2[1]/(500 / v.x_guide))
            # print(str(v.zone_x) + ' ' + str(v.zone_y))

    # returns only a list of the main 4 needed corners.. with an increment of 2, it is the corners of the inner square
    def get_marker_corners(self, inc=2):
        new_corners = []
        # inc = 2  # increment for which corner it should pick
        for i in range(4):
            index = np.where(self.ids == i)[0][0]
            new_corners.append((self.corners[index][0][(i + inc) % 4][0], self.corners[index][0][(i + inc) % 4][1]))
        self.final_corners = new_corners

# for testing
if __name__ == "__main__":
    img = cv2.imread('../images/saved/test/masked.jpg', -1)
    v.point2 = Detector.find_mask_point(img)
    Detector.find_zone()
    cv2.imshow('img', img)
    cv2.waitKey(0)

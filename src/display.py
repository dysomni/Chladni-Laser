#######################################################################################################################
# display.py
#
# This creates the windows for the user to see. It manipulates some images and adds guides just for the display
#
# Created by James Brock for Scott Hawley's Physics for AET class
#
# NOTE: SPECIFY ALL VARIABLES NEEDED IN THE VARIABLES.PY MODULE
#######################################################################################################################

import cv2
import numpy as np
import src.variables as v
from src.detector import Detector
import copy


# Class that manipulates images for display and displays them.
# There should be one object of this for each Imager object
class Display:

    # Creates a blank image as the store of the last image to be displayed, so that when no new capture information is
    # created, it will just show a blank screen until it receives that data
    lastReading = np.zeros((250, 500, 3), np.uint8)

    # output_size currently has no effect on the windows. They are all defaulting to 500x500 px
    def __init__(self, name, output_size):
        self.name = name
        self.window = cv2.namedWindow(name)
        self.output_size = output_size

    # Method to be called if the markers are detected. This takes all read images and prepares them for display
    # Parameters: img - raw image, drawn - original image but with aruco drawings, warp - warped images of inside marks
    #             mask - mask of warped image, point - a tuple of the detected point
    def detected(self, img, drawn, warp, mask, point=None):
        pmask = None  # mask with point superimposed
        mask2 = None  # initialized early - used for scaling the original mask

        if point is not None:  # if the point exists
            pmask = cv2.circle(copy.deepcopy(mask), point, 10, (0,255,0),5)  # draw a circle on the mask where it is
            mask2 = cv2.resize(pmask, (250, 250), fx=0, fy=0)  # show this scaled mask on the output
        else:  # if not, just use the original mask and scale it down to display
            mask2 = cv2.resize(mask, (250, 250), fx=0, fy=0)

        # self.update_variables(img, warp, mask, pmask=pmask)  # stores each image
        self.set_detected()  # changes variables to know we detected

        if self.name == v.INSTANCE_TWO_NAME:  # if the image being modified is for the reflective surface, draw guides
            warp = self.draw_guides(copy.deepcopy(warp), v.x_guide)

        # resize the images for display
        warp2 = cv2.resize(warp, (250, 250), fx=0, fy=0)
        img2 = cv2.resize(drawn, (500, 275), fx=0, fy=0)

        numpy_horizontal = np.hstack((warp2, mask2))  # add images horizontally

        self.lastReading = numpy_horizontal
        numpy_vertical = np.vstack((img2, numpy_horizontal))  # makes full image

        self.show(numpy_vertical)  # show it!
        return

    # If the markers are not detected, display image with last detected images
    def undetected(self, img):
        self.set_undetected()  # set variables to undetected
        img2 = cv2.resize(img, (500, 275), fx=0, fy=0)
        numpy_vertical = np.vstack((img2, self.lastReading))
        self.show(numpy_vertical)
        return

    # modifies variables.py variables depending on the name
    def set_detected(self):
        if self.name == v.INSTANCE_ONE_NAME:
            v.one_detected = True
        if self.name == v.INSTANCE_TWO_NAME:
            v.two_detected = True

    # modifies variables.py variables depending on the name
    def set_undetected(self):
        if self.name == v.INSTANCE_ONE_NAME:
            v.one_detected = False
        if self.name == v.INSTANCE_TWO_NAME:
            v.two_detected = False

    # stores each image passed in into the variables module depending on the name specified
    def update_variables(self, img, warp, mask, pmask=None):
        if self.name == v.INSTANCE_ONE_NAME:
            v.img1 = img
            v.warp1 = warp
            v.mask1 = mask
            v.pmask1 = mask
            if pmask is not None:
                v.pmask1 = pmask
        if self.name == v.INSTANCE_TWO_NAME:
            v.img2 = img
            v.warp2 = warp
            v.mask2 = mask
            v.pmask2 = mask
            if pmask is not None:
                v.pmask2 = pmask

    # wrapper for the cv2 imshow function
    def show(self, img):
        cv2.imshow(self.name, img)
        k = cv2.waitKey(1)
        if k == 27:  # if the key pressed is escape
            v.not_break = False
        if k == ord(' '):  # if the key pressed is the space - indicates a photo is to be taken
            v.take_pic = True
        if k == ord('p'):  # if the key pressed is a 'p' - indicates calibration and takes a photo
            v.take_pic = True
            v.point_adjust = True
        return

    # creates a new window to show the last images that were taken by the user
    def results(self):
        numpy_horizontal1 = np.hstack((v.warp1[0], v.pmask1[0]))
        numpy_horizontal2 = np.hstack((v.warp2[0], v.pmask2[0]))
        numpy_horizontal = np.hstack((numpy_horizontal1, numpy_horizontal2))
        img = cv2.resize(numpy_horizontal, (400, 100), fx=0, fy=0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = cv2.putText(img, str(v.zone_x) + '/' + str(v.zone_y), (10, 20), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        self.show(img)

    # draw guides on the reflective surface warped image so that you can line up the laser
    def draw_guides(self, img, x):
        for i in range(x):
            img = cv2.line(img, (int(500/x)*i, 0), (int(500/x)*i, 500), (0,0,255), 1)
            img = cv2.line(img, (0, int(500 / x) * i), (500, int(500 / x) * i), (0, 0, 255), 1)
        return img

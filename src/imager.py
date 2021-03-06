#######################################################################################################################
# imager.py
#
# Responsible for handling the detector, display, and export py modules as a single object
#
# Created by James Brock for Scott Hawley's Physics for AET class
#
# NOTE: SPECIFY ALL VARIABLES NEEDED IN THE VARIABLES.PY MODULE
#######################################################################################################################

import cv2
import src.detector as detector
import src.display as display
import src.variables as v
import src.export as export
# import src.gui as gui
import copy
import time


# Class to represent an image capture object that can run detection, etc
class Imager:

    object_list = []  # list used so that the class method can iterate over created objects
    # results_display = display.Display('results', (500,500))  # creates the display object for the results

    # name must be the instance name, because it is passed to all children objects
    # source is the index on which camera will be used by the VideoCapture object
    def __init__(self, name, source):
        self.name = name

        self.detect = detector.Detector(name)
        self.disp = display.Display(name, (500,500))

        Imager.object_list.append(self)
        self.cap = cv2.VideoCapture(source)
        self.cap.open(source)

    # close the image capture object
    def close(self):
        self.cap.release()
        return

    # take an image on just the one object
    def take(self):
        ret, self.img = self.cap.read()
        # if not ret:
        #     time.sleep(.5)
        #     ret, self.img = self.cap.read()

    # method that takes an image for each object ever created
    @classmethod
    def all_take(cls):
        for o in Imager.object_list:
            ret, o.img = o.cap.read()

    # runs the detection and manipulation on images, and then saves them
    @classmethod
    def all_detect(cls, interface1):
        # gui.update()
        v.point1 = None
        v.point2 = None
        for o in Imager.object_list:  # for each object
            if o.detect.detect_aruco_markers(o.img):  # run detection
                video = [None] * v.frame_amount
                warp = [None] * v.frame_amount
                mask = [None] * v.frame_amount
                for i in range(v.frame_amount):
                    o.take()
                    video[i] = o.img
                    warp[i] = o.detect.warp(o.img)  # create the warped image
                    mask_point = None
                    if o.name == v.INSTANCE_ONE_NAME:  # if its the non reflective surface
                        mask[i] = o.detect.mask(warp[i], interface1.threshold1)  # create the mask
                        if v.point_adjust:  # if it is set to calibrate
                            mask_point = detector.Detector.find_mask_point(mask[i])  # find the point on the mask
                            v.point1 = mask_point
                            o.disp.detected(o.img, o.detect.draw_aruco_markers(copy.deepcopy(o.img), big_outline=True),
                                            warp[i], mask[i], point=mask_point)
                            break

                    else:  # if it is for the reflective surface
                        mask[i] = o.detect.mask(warp[i], interface1.threshold2)  # create the mask
                        mask_point = detector.Detector.find_mask_point(mask)  # find the point from the mask
                        v.point2 = mask_point
                        o.disp.detected(o.img, o.detect.draw_aruco_markers(copy.deepcopy(o.img), big_outline=True),
                                        warp[i], mask[i], point=mask_point)
                        break

                    # display what we found!
                    o.disp.detected(video[i], o.detect.draw_aruco_markers(copy.deepcopy(video[i]), big_outline=True),
                                    warp[i], mask[i], point=mask_point)

                o.disp.update_variables(video, warp, mask)
                # print("15 frames")

            else:  # if the markers were not found: just show the captured image
                o.disp.undetected(o.img)

        # if both sets of markers were detected and the user wants to take a picture, save the images
        if v.one_detected and cls.consider_two and v.take_pic:
            detector.Detector.find_zone()
            export.save_images()
            # Imager.results_display.results()
        else:
            v.take_pic = False

    @classmethod
    def consider_two(cls):
        RPT = v.reflection_point_tracking
        TD = v.two_detected
        if RPT:
            return TD
        else:
            return True

#######################################################################################################################
# interface.py
#
# This creates and manages the GUI for the user to change values of the process
#
# Created by James Brock for Scott Hawley's Physics for AET class
#
# NOTE: SPECIFY ALL VARIABLES NEEDED IN THE VARIABLES.PY MODULE
#######################################################################################################################

import cv2
import src.timer as timer
import numpy as np
import src.variables as v

NAME_OF_WINDOW = 'parameters'


# Creates the GUI in addition to the children ThresholdControl objects
class Interface:

    param = np.zeros((1, 512, 3), np.uint8)  # creating a blank image that is needed for some reason to make a window
    parameters = cv2.namedWindow(NAME_OF_WINDOW)

    v.take_pic = False

    # v.const_mon = True  # currently isn't being used
    # timer1 = timer.Timer()  # currently isn't being used

    def __init__(self):
        # cv2.createTrackbar('take', 'parameters', 0, 1, self.take_pic_action)  # not being used
        # cv2.createTrackbar('monitor', 'parameters', 0, 1, self.monitor_action)  # not being used
        # cv2.setTrackbarPos('monitor', 'parameters', int(v.const_mon))  # not being used

        cv2.createTrackbar('angle', 'parameters', 0, 90, self.angle_action)
        cv2.setTrackbarPos('angle', 'parameters', int(v.REFLECTION_ANGLE))

        cv2.createTrackbar('distance', 'parameters', 0, 200, self.distance_action)
        cv2.setTrackbarPos('distance', 'parameters', int(v.REFLECTION_DISTANCE))

        cv2.createTrackbar('frequency', 'parameters', 1, 20000, self.frequency_action)
        cv2.setTrackbarPos('frequency', 'parameters', int(v.FREQUENCY))

        cv2.createTrackbar('x', 'parameters', 0, v.x_guide-1, self.x_action)
        cv2.setTrackbarPos('x', 'parameters', 0)
        cv2.createTrackbar('y', 'parameters', 0, v.x_guide - 1, self.y_action)
        cv2.setTrackbarPos('y', 'parameters', 0)

        # Creates the two thresholdControl children
        self.threshold1 = ThresholdControl(0, v.INSTANCE_ONE_NAME)
        self.threshold2 = None
        if v.reflection_point_tracking:
            self.threshold2 = ThresholdControl(1, v.INSTANCE_TWO_NAME)

        cv2.imshow(NAME_OF_WINDOW, self.param)  # Creates the window with the blank image we generated earlier

    def x_action(self, x):
        v.zone_x = x

    def y_action(self, x):
        v.zone_y = x

    def angle_action(self, x):
        v.REFLECTION_ANGLE = str(x)

    def frequency_action(self, x):
        v.FREQUENCY = str(x)

    def distance_action(self, x):
        v.REFLECTION_DISTANCE = str(x)

    # NOT BEING USED: #####
    # def take_pic_action(self, x):
    #     if self.timer1.hasItBeenASecond() and x == 1:
    #         v.take_pic = True
    #         return
    #     cv2.setTrackbarPos('take', 'parameters', 0)
    #     return
    #
    # def monitor_action(self, x):
    #     if x == 1:
    #         v.const_mon = True
    #     if x == 0:
    #         v.const_mon = False
    #     return
    #######################


# Class that houses the individual controls for each camera
class ThresholdControl:

    # Initializing the values of the sliders
    index = 0  # This is the identifier of
    # v.color_low[index] = 30
    # v.color_high[index] = 100
    # v.low_threshold[index] = 50

    # Parameters: index-identifier  name-identifier
    def __init__(self, index, name):
        self.name = name
        self.index = index
        # Creates each slider and sets its value to the default value we set earlier
        cv2.createTrackbar('color low' + str(index), NAME_OF_WINDOW, 0, 255, self.color_low_action)
        cv2.setTrackbarPos('color low'+str(index), NAME_OF_WINDOW, v.color_low[index])
        cv2.createTrackbar('color high' + str(index), NAME_OF_WINDOW, 0, 255, self.color_high_action)
        cv2.setTrackbarPos('color high'+str(index), NAME_OF_WINDOW, v.color_high[index])

        cv2.createTrackbar('sat low' + str(index), NAME_OF_WINDOW, 0, 255, self.sat_low_action)
        cv2.setTrackbarPos('sat low' + str(index), NAME_OF_WINDOW, v.sat_low[index])
        cv2.createTrackbar('sat high' + str(index), NAME_OF_WINDOW, 0, 255, self.sat_high_action)
        cv2.setTrackbarPos('sat high' + str(index), NAME_OF_WINDOW, v.sat_high[index])

        cv2.createTrackbar('val low' + str(index), NAME_OF_WINDOW, 0, 255, self.val_low_action)
        cv2.setTrackbarPos('val low' + str(index), NAME_OF_WINDOW, v.val_low[index])
        cv2.createTrackbar('val high' + str(index), NAME_OF_WINDOW, 0, 255, self.val_high_action)
        cv2.setTrackbarPos('val high' + str(index), NAME_OF_WINDOW, v.val_high[index])

        # cv2.createTrackbar('low threshold' + str(index), NAME_OF_WINDOW, 0, 255, self.low_threshold_action)
        # cv2.setTrackbarPos('low threshold'+str(index), NAME_OF_WINDOW, v.low_threshold[index])

    # These are the methods that are called whenever a slider is moved.
    # Each method sets the new value to the variable specified.
    def color_low_action(self, x):
        v.color_low[self.index] = x

    def color_high_action(self, x):
        v.color_high[self.index] = x

    def sat_low_action(self, x):
        v.sat_low[self.index] = x

    def sat_high_action(self, x):
        v.sat_high[self.index] = x

    def val_low_action(self, x):
        v.val_low[self.index] = x

    def val_high_action(self, x):
        v.val_high[self.index] = x


    def low_threshold_action(self, x):
        v.low_threshold[self.index] = x

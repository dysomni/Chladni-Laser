#######################################################################################################################
# __main__.py
#
# This is the main file that initiates the image capture process and maintains the process in a while loop
#
# Created by James Brock for Scott Hawley's Physics for AET class
#
# Instructions: Press space to take a photo and store results,
#               Press p to save point coordinates for each camera to calibrate the alignment
#               Press esc to end the program
#
# Purpose: to take, store, and process images of the reflection of a laser to be analyzed to map the x and y vibrations
#          of the reflecting surface at different frequencies
#
# NOTE: SPECIFY ALL VARIABLES NEEDED IN THE VARIABLES.PY MODULE
#######################################################################################################################

from cv2 import waitKey, destroyAllWindows
import src.generation as generation
import src.interface as interface
import src.imager as imager
import src.variables as v


if __name__ == '__main__':

    # This will be used if you need to generate new aruco markers.
    # -Second parameter is the number of markers to generate.
    # generation.genArucoMarkers(v.markerDictionary, 4)

    # Create instances of our needed classes: #####

    interface1 = interface.Interface()

    # These are the objects that will spawn the capture objects.
    # -Second parameter is the index of the capture device.
    # -With two webcams plugged in, the indices will be either 0, 1, or 2
    imager1 = imager.Imager(v.INSTANCE_ONE_NAME, 1)
    imager2 = imager.Imager(v.INSTANCE_TWO_NAME, 0)

    # Main loop:
    while True:
        imager.Imager.all_take()  # have each object take a photo
        imager.Imager.all_detect(interface1)  # run the detection, manipulation, and display of each image
        k = waitKey(1)  # wait one milliseconds and returns if any keys are pressed
        if k == 27:  # if the key pressed is escape
            break
        if k == ord(' '):  # if the key pressed is the space - indicates a photo is to be taken
            v.take_pic = True
        if k == ord('p'):  # if the key pressed is a 'p' - indicates calibration and takes a photo
            v.take_pic = True
            v.point_adjust = True

destroyAllWindows()

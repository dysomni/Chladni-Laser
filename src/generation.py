#######################################################################################################################
# generation.py
#
# This creates new aruco markers
#
# The set of markers I used is saved at ./images/gen/tracker.png
# The markers must be arranged in ascending index order clockwise starting from the top left corner of the full tracker
# Like so: (m is aruco marker)
#   m0  m1
#   m3  m2
#
# Created by James Brock for Scott Hawley's Physics for AET class
#######################################################################################################################

from cv2.aruco import drawMarker
from cv2 import imwrite


# Parameters: the marker dictionary needed, and the amount of markers to generate.
def genArucoMarkers(markerDictionary, amount):

    for i in range(amount):
        img = drawMarker(markerDictionary, i, 500)  # creates
        imwrite("../images/gen/marker" + str(i) + ".jpg", img)  # saves

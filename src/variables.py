#######################################################################################################################
# variables.py
#
# HERE IS WHERE YOU EDIT VARIABLES. DO NOT CHANGE THEM UNLESS YOU KNOW WHAT YOU ARE DOING
#
# Created by James Brock for Scott Hawley's Physics for AET class
#######################################################################################################################


from cv2.aruco import getPredefinedDictionary, DICT_4X4_50

# NAMING VARIABLES #############################

# CHANGE THESE
FOLDER_NAME = "Video_Testing"  # Folder within the 'saved' folder that all data will be stored
EXPERIMENT_NAME = "Second_Test"  # Name of the experiment
FREQUENCY = "389"  # Frequency used in the experiment
REFLECTION_DISTANCE = "18"  # distance from the dot on the plate to the wall in in
REFLECTION_ANGLE = "42"  # angle of incidence off of the plate in degrees

INSTANCE_ONE_NAME = "wall"  # This is the instance that will be capturing patterns on a surface
INSTANCE_TWO_NAME = "plate"  # This is the instance that will be capturing point information from the reflecting surface

# INTERFACE VARIABLES #########################

# Each index is for each Imager instance respectively
color_low = [30, 30]
color_high = [100, 100]

sat_low = [0,51]
sat_high = [255,255]

val_low = [67,183]
val_high = [172,255]

low_threshold = [50, 50]
take_pic = False
point_adjust = False
const_mon = True

# CHANGE THIS
reflection_point_tracking = False  # Opens a second Imager instance with for tracking the point of reflection

# DETECTION VARIABLES #########################

# CHANGE THIS
x_guide = 10  # This number squared is the number of measurements that you will have to take for each frequency.
frame_amount = 30  # The amount of frames to capture

one_detected = False
two_detected = False
zone_x = -1
zone_y = -1

# SAVED IMAGES ################################

img1 = None
img2 = None
warp1 = None
warp2 = None
mask1 = None
mask2 = None
pmask1 = None
pmask2 = None
point1 = None
point2 = None

# DICTIONARY VARIABLE ##########################

markerDictionary = getPredefinedDictionary(DICT_4X4_50)

not_break = True

gui_display = True
gui_displayed = [0] * (x_guide**2)


# Returns the number of the instance based on the input of the name
def get_number(name):
    if name == INSTANCE_ONE_NAME:
        return 0
    if name == INSTANCE_TWO_NAME:
        return 1
    return 0

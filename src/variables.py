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
FOLDER_NAME = "First_Meeting"  # Folder within the 'saved' folder that all data will be stored
EXPERIMENT_NAME = "First_Experiment"  # Name of the experiment
FREQUENCY = "500"  # Frequency used in the experiment
REFLECTION_DISTANCE = "4"  # distance from the dot on the plate to the wall in ft
REFLECTION_ANGLE = "45"  # angle of incidence off of the plate in degrees

INSTANCE_ONE_NAME = "wall"  # This is the instance that will be capturing patterns on a surface
INSTANCE_TWO_NAME = "plate"  # This is the instance that will be capturing point information from the reflecting surface

# INTERFACE VARIABLES #########################

color_low = [30, 30]
color_high = [100, 100]
low_threshold = [50, 50]
take_pic = False
point_adjust = False
const_mon = True

# DETECTION VARIABLES #########################

# CHANGE THIS
x_guide = 20  # This number squared is the number of measurements that you will have to take for each frequency.

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


# Returns the number of the instance based on the input of the name
def get_number(name):
    if name == INSTANCE_ONE_NAME:
        return 0
    if name == INSTANCE_TWO_NAME:
        return 1
    return 0

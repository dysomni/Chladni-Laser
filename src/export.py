#######################################################################################################################
# export.py
#
# This is responsible for the saving and storing of all information in the process.
# It will save images and a CSV based on the information in the variables module.
#
# DO NOT delete the generated .csv or .txt file unless you are willing to delete all the photos
#
# Created by James Brock for Scott Hawley's Physics for AET class
#
# NOTE: SPECIFY ALL VARIABLES NEEDED IN THE VARIABLES.PY MODULE
#######################################################################################################################

from cv2 import imwrite
import csv
import os
import src.variables as v
import datetime


# Method that is called to initiate the saving of all images captured and processed
def save_images():

    # Checks to see if the folder specified from the variables module exists and if not, creates it
    if not os.path.exists('../images/saved/' + v.FOLDER_NAME):
        os.makedirs('../images/saved/' + v.FOLDER_NAME)

    # checks to see if the .txt file that stores the image index exists, if not, it creates it, if so, it increments it
    if os.path.isfile('../images/saved/' + v.FOLDER_NAME + '/' + v.EXPERIMENT_NAME + '_index.txt'):
        file = open('../images/saved/' + v.FOLDER_NAME + '/' + v.EXPERIMENT_NAME + '_index.txt', 'r')
        ind = int(file.read())
        file.close()
        ind = ind + 1
        file = open('../images/saved/' + v.FOLDER_NAME + '/' + v.EXPERIMENT_NAME + '_index.txt', 'w')
        file.write(str(ind))
        file.close()
    else:
        file = open('../images/saved/' + v.FOLDER_NAME + '/' + v.EXPERIMENT_NAME + '_index.txt', 'x')
        file.close()
        file = open('../images/saved/' + v.FOLDER_NAME + '/' + v.EXPERIMENT_NAME + '_index.txt', 'w')
        ind = 1
        file.write(str(ind))
        file.close()

    # Saving of all the images stored in the variables module
    imwrite('../images/saved/' + v.FOLDER_NAME + '/' + v.EXPERIMENT_NAME + '_' + str(ind) + '_img_1.jpg', v.img1)
    imwrite('../images/saved/' + v.FOLDER_NAME + '/' + v.EXPERIMENT_NAME + '_' + str(ind) + '_warp_1.jpg', v.warp1)
    imwrite('../images/saved/' + v.FOLDER_NAME + '/' + v.EXPERIMENT_NAME + '_' + str(ind) + '_mask_1.jpg', v.mask1)
    imwrite('../images/saved/' + v.FOLDER_NAME + '/' + v.EXPERIMENT_NAME + '_' + str(ind) + '_img_2.jpg', v.img2)
    imwrite('../images/saved/' + v.FOLDER_NAME + '/' + v.EXPERIMENT_NAME + '_' + str(ind) + '_warp_2.jpg', v.warp2)
    imwrite('../images/saved/' + v.FOLDER_NAME + '/' + v.EXPERIMENT_NAME + '_' + str(ind) + '_mask_2.jpg', v.mask2)

    # Data list as strings that will be passed into the .csv file
    data = [
        str(ind),
        str(v.x_guide),
        str(v.zone_x),
        str(v.zone_y),
        str(v.point1),
        str(v.point2),
        str(v.point_adjust),
        str(datetime.datetime.now()),
        v.FREQUENCY,
        v.REFLECTION_ANGLE,
        v.REFLECTION_DISTANCE,
        v.FOLDER_NAME,
        v.EXPERIMENT_NAME,
        v.INSTANCE_ONE_NAME,
        v.INSTANCE_TWO_NAME,
    ]

    # Checks to see if the .csv file exists, if not, creates one and writes the header to it
    if not os.path.isfile('../images/saved/' + v.FOLDER_NAME + '/' + v.EXPERIMENT_NAME + '_logs.csv'):
        file = open('../images/saved/' + v.FOLDER_NAME + '/' + v.EXPERIMENT_NAME + '_logs.csv', 'x')
        file.close()
        file = open('../images/saved/' + v.FOLDER_NAME + '/' + v.EXPERIMENT_NAME + '_logs.csv', 'w')
        file.write("index,zone#,x_zone,y_zone,point1,point2,point_calibration,date,frequency,angle,distance,folder,experiment,instance_one,instance_two\n")
        file.close()

    # Writes the values specified in 'data' to the .csv
    with open('../images/saved/' + v.FOLDER_NAME + '/' + v.EXPERIMENT_NAME + '_logs.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerows([data])

    # Returns the picture initiation variables back to False to make sure it doesn't continue taking photos
    v.take_pic = False
    v.point_adjust = False

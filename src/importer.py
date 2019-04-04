import cv2
import numpy as np
import src.variables as v
import src.interface as interface
import itertools as itr
import statistics as stat
import math


def threshold_testing():

    # v.FOLDER_NAME = ""
    # v.EXPERIMENT_NAME = ""

    parameters = cv2.namedWindow(interface.NAME_OF_WINDOW)
    param_controls = interface.ThresholdControl(0, "Threshold Testing")
    cont = True
    ind = 1

    while cont:
        filename_head = '../images/saved/' + v.FOLDER_NAME + '/' + v.EXPERIMENT_NAME + '_' + str(ind)
        playback = cv2.VideoCapture(filename_head + '_warp_1.avi')
        if not playback.isOpened():
            print("Error opening video stream or file")
        images_loop = []
        masks_loop = []
        ret = True
        while ret:
            ret, frame = playback.read()
            if ret:
                images_loop.append(frame)

        for frame in images_loop:
            masks_loop.append(get_mask(frame))

        add = masks_loop[0]
        for frame in masks_loop:
            add += frame
        point = find_mask_point(add)
        # x_avg = find_x_avg(add, point)
        # y_avg = find_y_avg(add, point)
        x_avg, y_avg, point1, point2, delta_theta_x, delta_theta_y = find_farthest_points(add, point)

        draw_point = False
        for frame in itr.cycle(images_loop):
            frame2 = get_mask(frame)
            if np.array_equal(frame, images_loop[0]):
                add = frame2
            else: add += frame2
            cv2.imshow('Playback', frame)
            cv2.imshow('Playback2', frame2)
            add = cv2.circle(add, point, 10, (0, 255, 0), 5)
            add = cv2.line(add, (point[0]-x_avg, point[1]), (point[0]+x_avg, point[1]), (0, 255, 0), 2)
            add = cv2.line(add, (point[0], point[1] - y_avg), (point[0], point[1] + y_avg), (0, 255, 0), 2)
            add = cv2.line(add, point1, point2, (0, 0, 255), 4)
            font = cv2.FONT_HERSHEY_SIMPLEX
            add = cv2.putText(add, 'average delta angles  - x:' + str('%.3f' % (delta_theta_x)) + ' y:' + str(
                '%.3f' % (delta_theta_y) + ' (degrees)'), (10, 20), font, 0.5, (0, 0, 0), 1,
                              cv2.LINE_AA)
            add = cv2.putText(add, 'average displacement - x:' + str('%.3f' % (x_avg * 2 / 125)) + ' y:' + str(
                '%.3f' % (y_avg * 2 / 125)) + ' (inches)', (10, 40), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            add = cv2.putText(add, 'average delta angles  - x:' + str('%.3f'%(delta_theta_x)) + ' y:' + str('%.3f'%(delta_theta_y) + ' (degrees)'), (10, 20), font, 0.5, (255, 0, 0), 1,
                              cv2.LINE_AA)
            add = cv2.putText(add, 'average displacement - x:' + str('%.3f' % (x_avg*2/125)) + ' y:' + str(
                '%.3f' % (y_avg*2/125)) + ' (inches)', (10, 40), font, 0.5, (255, 0, 0), 1,cv2.LINE_AA)
            cv2.imshow('Result', add)

            k = cv2.waitKey(50)
            if k is ord(' '):
                break
            if k == 27:  # if the key pressed is escape
                cont = False

        playback.release()
        ind += 1


def get_mask(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_color = np.array([v.color_low[0], v.sat_low[0], v.val_low[0]])
    upper_color = np.array([v.color_high[0], v.sat_high[0], v.val_high[0]])
    ret = cv2.inRange(img, lower_color, upper_color)
    ret = cv2.cvtColor(ret, cv2.COLOR_GRAY2BGR)
    return ret


def find_mask_point(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    point = (0,0)
    points = []
    for i in range(500):  # relies on the image being 500x500 px
        for j in range(500):
            if img[i][j] > 200:
                points.append((i,j))
    if len(points) == 0:
        return None
    points = np.array(points)
    point = np.mean(points, axis=0, dtype=int)
    point = (point[1],point[0])
    return point


def find_farthest_points(img, center):
    d = 20
    theta = 32
    point1 = None
    point2 = None
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    t_points = []
    b_points = []
    l_points = []
    r_points = []
    for i in range(center[0]):  # relies on the image being 500x500 px
        for j in range(500):
            if img[i][j] > 200:
                t_points.append((i, j))
                img[i][j] = 0
    for i in range(500 - center[0]):  # relies on the image being 500x500 px
        for j in range(500):
            if img[499 - i][j] > 200:
                b_points.append((499 - i, j))
                # img[i][499-j] = 0
    for i in range(500):  # relies on the image being 500x500 px
        for j in range(center[0]):
            if img[i][j] > 200:
                l_points.append((i,j))
                # img[i][j] = 0
    for i in range(500):  # relies on the image being 500x500 px
        for j in range(500-center[0]):
            if img[i][499-j] > 200:
                r_points.append((i,499-j))
                # img[i][499-j] = 0

    t_points = np.array(t_points)
    b_points = np.array(b_points)
    tpoint = (np.mean(t_points, axis=0, dtype=int))
    t = tpoint[0]
    bpoint = (np.mean(b_points, axis=0, dtype=int))
    b = bpoint[0]
    t = abs(center[0] - t)
    b_y_d = abs(center[0] - b)
    # point = (point[1],point[0])
    y_avg = int((t + b_y_d) / 2)

    l_points = np.array(l_points)
    r_points = np.array(r_points)
    lpoint = (np.mean(l_points, axis=0, dtype=int))
    l = lpoint[1]
    rpoint = (np.mean(r_points, axis=0, dtype=int))
    r = rpoint[1]
    l_x_d = abs(center[0] - l)
    r_x_d = abs(center[0] - r)
    # point = (point[1],point[0])
    x_avg = int((l_x_d + r_x_d) / 2)

    m = 0
    dif = 0
    if x_avg >= y_avg:
        point1 = (lpoint[1],lpoint[0])
        point2 = (rpoint[1],rpoint[0])
        m = slope(point1[0], point1[1], point2[0], point2[1])
        dif = x_avg - y_avg

    else:
        point1 = (tpoint[1],tpoint[0])
        point2 = (bpoint[1],bpoint[0])
        m = slope(point1[0], point1[1], point2[0], point2[1])
        dif = y_avg - x_avg

    dif = dif*2

    point1 = (
        int(((dif * math.sin(math.atan(m))) / m) + center[0]), int(m * (dif * math.cos(math.atan(m))) + center[1]))
    point2 = (
        int(((-dif * math.sin(math.atan(m))) / m) + center[0]), int(m * (-dif * math.cos(math.atan(m))) + center[1]))

    # point1 = (stat.mean([tpoint[1],lpoint[1]]),stat.mean([tpoint[0],lpoint[0]]))
    # point2 = (stat.mean([bpoint[1], rpoint[1]]), stat.mean([bpoint[0], rpoint[0]]))

    delta_theta_x = math.degrees(math.atan((x_avg/125)/d))
    delta_theta_y = math.degrees(math.atan(((math.tan(math.radians(theta))/d)+(y_avg/125))/d))

    return x_avg, y_avg, point1, point2, delta_theta_x, delta_theta_y

def slope(x1, y1, x2, y2):
    m = (y2-y1)/(x2-x1)
    return m

if __name__ == '__main__':
    threshold_testing()
    print("Hello")

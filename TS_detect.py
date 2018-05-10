import cv2
import mss
import imutils
import os
import sys
import time
import datetime
from imutils import contours
import numpy as np

def referenceGrabber(n=0):
    return

def grabber(pair_title,n,sct):
    top, left = 20, 4
    width, height = 72, 119
    monitor_number = 2
    mon = sct.monitors[monitor_number]

    monitor_TS_new = {'top':mon['top']+top, 'left':mon['left']+left+width*n, 'width':width, 'height':height, 'mon': monitor_number,}
    monitor_TS_old = {'top':mon['top']+top + height, 'left':mon['left']+left+width*n, 'width':width, 'height':height, 'mon': monitor_number,}

    frame_TS_new_raw = np.array(sct.grab(monitor_TS_new))
    frame_TS_new = cv2.cvtColor(frame_TS_new_raw, cv2.COLOR_RGBA2RGB)

    frame_TS_old_raw = np.array(sct.grab(monitor_TS_old))
    frame_TS_old = cv2.cvtColor(frame_TS_old_raw, cv2.COLOR_RGBA2RGB)

    # create bounds for color detection
    green_lower_range, green_upper_range = np.array([0,15,0]), np.array([10,255,10])
    red_lower_range, red_upper_range = np.array([0,0,30]), np.array([85,100,255])
    red_lower_range_old, red_upper_range_old = np.array([0,0,120]), np.array([10,10,255])

    # color mask each TS region
    green_mask_TS_new = cv2.inRange(frame_TS_new,green_lower_range, green_upper_range)
    red_mask_TS_new = cv2.inRange(frame_TS_new,red_lower_range, red_upper_range)

    green_mask_TS_old = cv2.inRange(frame_TS_old,green_lower_range, green_upper_range)
    red_mask_TS_old = cv2.inRange(frame_TS_old,red_lower_range_old, red_upper_range_old)

    # find contours for Old TS
    cnts_green_old = cv2.findContours(green_mask_TS_old.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts_green_old = cnts_green_old[0] if imutils.is_cv2() else cnts_green_old[1]

    cnts_red_old = cv2.findContours(red_mask_TS_old.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts_red_old = cnts_red_old[0] if imutils.is_cv2() else cnts_red_old[1]

    # count the number of green/red or zero boxes for Old TS
    filename = pair_title+' old.txt'
    here = os.path.dirname(os.path.realpath(__file__))
    subdir = 'files'
    fullpath = os.path.join(here, subdir, filename)
    green_bars=0
    red_bars=0
    if len(cnts_green_old) > 0:
        for c in cnts_green_old:
            if cv2.contourArea(c) > 100:
                green_bars +=1
        if green_bars > 0:
            try:
                with open(fullpath, 'w') as f:
                    f.write(str(green_bars))
            except PermissionError as err:
                print("OS error: {0}".format(err))

    elif len(cnts_red_old) > 0:
        for c in cnts_red_old:
            if cv2.contourArea(c) > 100:
                red_bars -=1
        if red_bars < 0:
            try:
                with open(fullpath, 'w') as f:
                    f.write(str(red_bars))
            except PermissionError as err:
                print("OS error: {0}".format(err))

    if green_bars == 0 & red_bars == 0:
        if time.time() > os.path.getmtime(fullpath) + 300: # 5 min persist
            try:
                with open(fullpath, 'w') as f:
                    f.write('0')
            except PermissionError as err:
                print("OS error: {0}".format(err))


    # find contours for New TS
    cnts_green_new = cv2.findContours(green_mask_TS_new.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts_green_new = cnts_green_new[0] if imutils.is_cv2() else cnts_green_new[1]

    cnts_red_new = cv2.findContours(red_mask_TS_new.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts_red_new = cnts_red_new[0] if imutils.is_cv2() else cnts_red_new[1]

    # save New TS values
    filename = pair_title+' new.txt'
    here = os.path.dirname(os.path.realpath(__file__))
    subdir = 'files'
    fullpath = os.path.join(here, subdir, filename)
    zero_green, zero_red = True, True
    if len(cnts_green_new) > 0:
        for c in cnts_green_new:
            # if the contour is not sufficiently large, ignore it
            if cv2.contourArea(c) > 175:
                zero_green = False
                area = cv2.contourArea(c)
                try:
                    with open(fullpath, 'w') as f:
                        f.write(str(area))
                except PermissionError as err:
                    print("OS error: {0}".format(err))

    elif len(cnts_red_new) > 0:
        for c in cnts_red_new:
            # if the contour is not sufficiently large, ignore it
            if cv2.contourArea(c) > 175:
                zero_red = False
                area = cv2.contourArea(c)
                try:
                    with open(fullpath, 'w') as f:
                        f.write('-'+str(area))

                except PermissionError as err:
                    print("OS error: {0}".format(err))

    if zero_green == True and zero_red == True:
        try:
            with open(fullpath, 'w') as f:
                f.write('0')
        except PermissionError as err:
            print("OS error: {0}".format(err))

    #cv2.imshow("Green TS New Raw", green_mask_TS_new)
    #cv2.imshow("Green TS Old Raw", green_mask_TS_old)
    #cv2.imshow("Red TS New Raw", red_mask_TS_new)
    #cv2.imshow("Red TS Old Raw", red_mask_TS_old)

#FX_pairs_list = ['REF':0,'GU':1, 'EU':2,'UJ':3,'UC':4,'CL':5,'DX':6]

def main():
    time_now=0
    while True:
        with mss.mss() as sct:

            grabber('GU',1,sct)
            grabber('EU',2,sct)
            grabber('UJ',3,sct)
            grabber('UC',4,sct)
            grabber('CL',5,sct)
            grabber('DX',6,sct)


            #time.sleep(1)
            if time.time() > time_now + 10:
                t = datetime.datetime.now()
                s = t.strftime('%Y.%m.%d %H:%M:%S.%f')
                time_now = s[:-4]
                print('TS Detect running at ' + time_now + '...')
                time_now=time.time()

if __name__ == '__main__':
    main()

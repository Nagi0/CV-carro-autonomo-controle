from MotorModule import Motor
import KeyPressModule as kp
import ColorModule as cm
import ContourModule as cnm
from time import sleep
import cv2
import numpy as np
import os

motor = Motor(2,3,4,17,22,27)


kp.init()
img = cv2.VideoCapture(0)
# img.set(3, 640)
# img.set(4, 480)
fourcc = cv2.VideoWriter_fourcc(*'XVID')

record_flag = False
record_counter = 0

hsv_values = [[92, 167, 51], [136, 255, 255]] # [[83, 84, 96], [134, 255, 255]]
prev_error = 0

def track_object(img, contours_found, pid, prev_error):
    if len(contours_found) != 0:
        x, y, w, h = contours_found[0][2]
        area = contours_found[0][1]
        if area < 10000.0:
            move = 0.45
        elif 10000.0 <= area < 30000.0:
            move = 0.4
        elif 30000.0 <= area < 50000 :
            move = 0.1
        else:
            move = 0.0
        #print(area)
        print(move)
        # print(x)
        cx = x + (w//2)
        cy = y + (h//2)

        hi, wi, ci = img.shape
        cv2.line(img, (wi//2, cy), (cx, cy), (255, 0, 255), 2)

        error = (wi//2) - cx
        pos_x = round((pid[0] * error) + (pid[1]*(error - prev_error)), 1)
        pos_x = round(np.interp(pos_x, [-w//4, w//4], [-0.45, 0.45]), 1)
        prev_error = error
        # print(pos_x)
        motor.moveF(move, -pos_x, 0.0001)
    else:
        motor.stop(0.0001)
        move = 0

    return img, prev_error

while True:
    ret, cap = img.read()

    mask, img_color = cm.findColor(cap, hsv_values)
    img_contours, contours_found = cnm.findContours(cap, mask, 500, drawCon=False)

    h, w, c = img_contours.shape
    cv2.line(img_contours, (w//2, 0), (w//2, h), (255, 0, 255), 2)

    img_contours, prev_error = track_object(img_contours, contours_found, [1/10, 1/8], prev_error)

    if record_flag:
        output.write(cap)

    # cv2.imshow('camera', cap)
    cv2.imshow('contours', img_contours)
    # cv2.imshow('img_color', img_color)
    k = cv2.waitKey(1)

    if k == 27:
        print('Código Encerrado')
        break

    elif k == ord('r'):
        print('Gravação Iniciada')
        output = cv2.VideoWriter(f'/home/pi/Desktop/self_driving_car/opencv_capture{record_counter}.avi', fourcc, 30, (640, 480))
        record_flag = True

    elif k == ord('s'):
        print('Gravação Salva')
        output.release()
        record_flag = False
        record_counter += 1

    if kp.get_key('UP'):
        motor.moveF(0.5, 0, 0.0001)

    elif kp.get_key('LEFT'):
        motor.moveF(0.5, 0.3, 0.0001)

    elif kp.get_key('RIGHT'):
        motor.moveF(0.5, -0.3, 0.0001)

    elif kp.get_key('DOWN'):
        motor.moveF(-0.5, 0, 0.0001)

    else:
        motor.stop(0.0001)


cv2.destroyAllWindows()

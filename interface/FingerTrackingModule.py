import cv2
import time
import math
import serial
import HandTrackingModule as htm
from resize import formattingImage, crop, transform
from transform import four_point_transform
from numpy import *
import krest_trest
import telnetlib

cap = cv2.VideoCapture(0)

overlayList = []

pTime = 0

detector = htm.handDetector()
cropCheck = True
tipIds = [4, 8, 12, 16, 20]

point = []

cropOn = False
flag_open = True
flag_rotate = True
y_robot_last = []
flag = False
fla = True


def y_robot_smoothing(y_robot):
    global y_robot_last
    if len(y_robot_last) > 0:
        y_robot_new = (y_robot_last[-1] - y_robot) / 2
        y_robot_last.append(y_robot_new)
        return y_robot
    else:
        y_robot_last.append(y_robot)
        return y_robot


last_angle = -999
open_ = 0
rotate_num = 90
rotate = 0

robot_ip = '192.168.43.54'
w = 0.07 # длина сустава
L = 74 # расстояние между камерой и полем в см
while True:
    siuccess, img = cap.read()
    try:
        point = crop(img)

        warped = four_point_transform(img, point)
        img = cv2.resize(warped, (int(600), int(600)),
                         interpolation=cv2.INTER_CUBIC)

        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            id = 9
            img = cv2.circle(img, (lmList[9][1], lmList[9][2]), radius=5, color=(100, 40, 40), thickness=-1)
            img = cv2.circle(img, (lmList[0][1], lmList[0][2]), radius=5, color=(100, 40, 40), thickness=-1)

            print(lmList[9][1], lmList[9][2])
            print(lmList[0][1], lmList[0][2])

            x = int(lmList[9][1]) * 2.5
            y = int(lmList[9][2]) * 2.5

            rxox = 600
            rxoy = 0

            trox = x
            troy = y
            try:
                angle = math.atan((rxoy - troy) / (rxox - trox))
            except:
                angle = 90
            x1 = rxox  # начало
            x2 = trox  # конец
            if x1 > x2:
                angle += math.pi

            angle = round(math.degrees(angle))

            x_robot = -round(((math.fabs(math.sqrt((x - 600) ** 2 + (y - 0) ** 2))) / 40), 2)
            x_robot += 0.02

            f = 845.714285714


            dis = math.sqrt(((lmList[9][1] - lmList[0][1]) * (lmList[9][1] - lmList[0][1])) + (
                        (lmList[9][2] - lmList[0][2]) * (lmList[9][2] - lmList[0][2])))
            y_robot = L - ((w * f) / dis) * 100


            fingers = []

            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            if fingers[1] == 1 and flag_open == True:
                open_ -= 1
                if open_ < 5:
                    telnet = telnetlib.Telnet(robot_ip)
                    telnet.write(b'F70')
                    flag_open = False
            elif fingers[1] == 0 and flag_open == False:
                open_ += 1
                if open_ > 5:
                    telnet = telnetlib.Telnet(robot_ip)
                    telnet.write(b'F180')
                    time.sleep(0.3)
                    telnet.write(b'F90')
                    flag_open = True

            if fingers[2] == 1:
                telnet = telnetlib.Telnet(robot_ip)
                telnet.write(b'E95')
                flag = True
                time.sleep(0.05)
            elif fingers[3] == 1:
                telnet = telnetlib.Telnet(robot_ip)
                telnet.write(b'E80')
                flag = True
                time.sleep(0.05)
            else:
                if flag:
                    telnet = telnetlib.Telnet(robot_ip)
                    telnet.write(b'E90')
                    flag = False
                    time.sleep(0.05)

            if fingers[4] == 1:
                telnet = telnetlib.Telnet(robot_ip)
                s = f'D{rotate_num}'
                telnet.write(s.encode())
                if fla == True:
                    rotate_num += 15
                else:
                    rotate_num -= 15
                if rotate_num > 180:
                    fla = False
                elif rotate_num < 10:
                    fla = True

                time.sleep(0.05)

            cv2.putText(img, str(fingers), (10, 70), cv2.FONT_HERSHEY_PLAIN,
                        3, (255, 0, 0), 3)

            cv2.putText(img, str(y_robot), (10, 170), cv2.FONT_HERSHEY_PLAIN,
                        3, (255, 0, 0), 3)

            if angle < 180:
                krest_trest.go_to([x_robot, y_robot], angle, flag_rotate)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.imshow("Image", img)
        cv2.waitKey(1)
    except:
        pass

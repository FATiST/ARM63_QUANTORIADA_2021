from os import name
from PyQt5 import QtGui
from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication, QLabel, QVBoxLayout, QListWidget, QSizePolicy, \
    QHBoxLayout, QListWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5 import uic, QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import sys
import cv2
import time
import math
import sqlite3
import HandTrackingModule as htm
from resize import formattingImage, crop, transform
from transform import four_point_transform
from numpy import *
import krest_trest
import telnetlib
import sys
import time
from termcolor import colored
import speech_recognition
import random
import traceback
import logging
import logging.config
import datetime

today = datetime.datetime.today()
time_ = today.strftime("%Y-%m-%d-%H-%M-%S")
name = f'logs/{time_}.log'
dictLogConfig = {
    "version": 1,
    "handlers": {
        "fileHandler": {
            "class": "logging.FileHandler",
            "formatter": "myFormatter",
            "filename": name
        }
    },
    "loggers": {
        "interface": {
            "handlers": ["fileHandler"],
            "level": "INFO",
        }
    },
    "formatters": {
        "myFormatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }
}

logging.config.dictConfig(dictLogConfig)
logger = logging.getLogger("interface")
logger.info("Program started")
logger.info("Done!")


class AudioThread(QThread):
    check = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self._record_start = False
        self.new_script = str()
        self.recognizer = speech_recognition.Recognizer()
        self.microphone = speech_recognition.Microphone()

    def run(self):
        while True:
            if self._run_flag:
                with self.microphone:
                    recognized_data = ""
                    self.recognizer.adjust_for_ambient_noise(self.microphone, duration=2)

                    try:
                        print("Listening...")
                        audio = self.recognizer.listen(self.microphone, 2, 3)

                        with open("microphone-results.wav", "wb") as file:
                            file.write(audio.get_wav_data())

                    except speech_recognition.WaitTimeoutError:
                        traceback.print_exc()

                    try:
                        print("Started recognition...")
                        recognized_data = self.recognizer.recognize_google(audio, language='ru').lower()
                        print(recognized_data)

                    except speech_recognition.UnknownValueError:
                        pass

                    except speech_recognition.RequestError:
                        print(colored("Trying to use offline recognition...", "cyan"))

                        print("Converting Speech to Text...")
                    if 1 < 2:
                        text = recognized_data
                        zazahvat = ['взять захват', 'пять захват', 'автопарк', 'взять закладку', 'взять зарплату',
                                    'возьми закон', 'захват']
                        bolt = ['Bolt взять', 'bolt взять', 'возьми болт', 'взять болт', 'болт', 'взять бомбу', 'бомбу',
                                'волк', 'gold']
                        marker = ['взять маркер', 'маркер', 'писать марки', 'марки', 'Маркет', 'market']
                        bolt20 = ['закрути', 'закрутить']
                        bolt20remove = ['убери', 'убрать']
                        illuminator = ['протри', 'протереть', 'окна', 'окно']
                        krest = ['нарисуй', 'крест', 'рисуй', 'нарисовать']
                        if text in zazahvat:
                            print('Взял захват')
                            logger.info("Распознана команда голосом: захват")
                            self.check.emit('Взял захват')
                        elif text in bolt:
                            print('Взял болт')
                            logger.info("Распознана команда голосом: болт")
                            self.check.emit('Взял болт')
                        elif text in marker:
                            print('Взял маркер')
                            logger.info("Распознана команда голосом: маркер")
                            self.check.emit('Взял маркер')
                        elif text in bolt20:
                            print('Болт20')
                            logger.info("Распознана команда голосом: вкрутить болт 20*20*20")
                            self.check.emit('Болт20')
                        elif text in bolt20remove:
                            print('Убрать болт 20')
                            logger.info("Распознана команда голосом: убрать болт 20*20*20")
                            self.check.emit('Болт20У')
                        elif text in illuminator:
                            print('Протирка')
                            logger.info("Распознана команда голосом: Протирка")
                            self.check.emit('Протирка')
                        elif text in krest:
                            print('Рисую')
                            logger.info("Распознана команда голосом: Нарисовать крест")
                            self.check.emit('Рисую')
                        else:
                            for i in text.split():
                                if i in zazahvat:
                                    print('Взял захват')
                                    logger.info("Распознана команда голосом: захват")
                                    self.check.emit('Взял захват')
                                elif i in bolt:
                                    print('Взял болт')
                                    logger.info("Распознана команда голосом: болт")
                                    self.check.emit('Взял болт')
                                elif i in marker:
                                    print('Взял маркер')
                                    logger.info("Распознана команда голосом: маркер")
                                    self.check.emit('Взял маркер')
                                elif i in bolt20:
                                    print('Болт20')
                                    logger.info("Распознана команда голосом: вкрутить болт 20*20*20")
                                    self.check.emit('Болт20')
                                elif i in bolt20remove:
                                    print('Убрать болт 20')
                                    logger.info("Распознана команда голосом: убрать болт 20*20*20")
                                    self.check.emit('Болт20У')
                                elif i in illuminator:
                                    print('Протирка')
                                    logger.info("Распознана команда голосом: Протирка")
                                    self.check.emit('Протирка')
                                elif i in krest:
                                    print('Рисую')
                                    logger.info("Распознана команда голосом: Нарисовать крест")
                                    self.check.emit('Рисую')
            else:
                pass


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    angle_ik = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self._record_start = False
        self.new_script = str()

    def run(self):
        cap = cv2.VideoCapture(0)
        pTime = 0
        detector = htm.handDetector()
        tipIds = [4, 8, 12, 16, 20]
        rotate_num = 90
        self.noArm = 0
        self.parkFlag = True
        flag_rotate = True
        first_start = True
        first_dis = 0
        while True:
            conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
            cursor = conn.cursor()
            cursor.execute(f'SELECT tool from info WHERE id = {1}')
            self.tool = cursor.fetchall()[0][0]
            siuccess, img = cap.read()
            if self._run_flag:
                if first_start:
                    try:
                        point = crop(img)
                        warped = four_point_transform(img, point)
                        img = cv2.resize(warped, (int(600), int(700)),
                                         interpolation=cv2.INTER_CUBIC)
                        img = detector.findHands(img)
                        lmList = detector.findPosition(img, draw=False)
                        if len(lmList) != 0:
                            self.parkFlag = True
                            self.noArm = 0
                            id = 9
                            img = cv2.circle(img, (lmList[5][1], lmList[5][2]), radius=5, color=(100, 40, 40),
                                             thickness=-1)
                            img = cv2.circle(img, (lmList[17][1], lmList[17][2]), radius=5, color=(100, 40, 40),
                                             thickness=-1)
                            x = int(lmList[9][1]) * 2.5
                            y = int(lmList[9][2]) * 2.5
                            rxox = 300
                            rxoy = 0
                            trox = x
                            troy = y
                            try:
                                angle = math.atan((rxoy - troy) / (rxox - trox))
                            except:
                                angle = 90
                            x1 = rxox
                            x2 = trox
                            if x1 > x2:
                                angle += math.pi
                            angle = round(math.degrees(angle))
                            x_robot = -round(((math.fabs(math.sqrt((x - 600) ** 2 + (y - 0) ** 2))) / 40), 2)
                            x_robot += 0.02
                            f = 1233
                            w = 0.07
                            dis = math.sqrt(((lmList[5][1] - lmList[17][1]) * (lmList[5][1] - lmList[17][1])) + (
                                    (lmList[5][2] - lmList[17][2]) * (lmList[5][2] - lmList[17][2])))
                            twoo_dis = dis
                            first_dis = math.sqrt(((lmList[5][1] - lmList[8][1]) * (lmList[5][1] - lmList[8][1])) + (
                                    (lmList[5][2] - lmList[8][2]) * (lmList[5][2] - lmList[8][2])))
                            print(dis)
                            y_robot = 90 - ((7 * f) / dis)
                            if y_robot >= -20 and y_robot <= 8:
                                if rotate_num > 145:
                                    y_robot = 0
                                else:
                                    y_robot = 8
                            elif y_robot >= 8 and y_robot <= 25:
                                y_robot = 17.5
                            elif y_robot >= 25 and y_robot <= 30:
                                y_robot = 27.5
                            else:
                                y_robot = 12.5
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
                            cv2.putText(img, str(first_dis), (10, 70), cv2.FONT_HERSHEY_PLAIN,
                                        3, (255, 0, 0), 3)
                            cv2.putText(img, str(y_robot), (10, 170), cv2.FONT_HERSHEY_PLAIN,
                                        3, (255, 0, 0), 3)

                            if angle < 180:
                                angle_ik = krest_trest.go_to([x_robot, y_robot], angle, flag_rotate)
                                logger.info(
                                    f'Передвижение в точку: {[x_robot, y_robot], angle, flag_rotate} Инструмент: {self.tool}')
                                a = angle_ik.split()
                                normal_ik = str()
                                angle_motor = a[1][1:]
                                for i in a[2:-1]:
                                    normal_ik += f"{str(i)} "
                                if self._record_start:
                                    self.new_script += f"{angle_ik} \n"
                        else:
                            if self.noArm >= 40 and self.parkFlag:
                                logger.info("Ушел в сон")
                                self.parkFlag = False
                                str_send = f"B60"
                                telnet = telnetlib.Telnet('192.168.1.159')
                                telnet.write(str_send.encode())
                                logger.info(str_send)
                                time.sleep(2)
                                str_send = 'C90'
                                telnet.write(str_send.encode())
                                logger.info(str_send)
                                time.sleep(2)
                                str_send = 'A90'
                                telnet.write(str_send.encode())
                                logger.info(str_send)
                                time.sleep(2)

                                str_send = 'D150 B55 C8'
                                telnet.write(str_send.encode())
                                logger.info(str_send)
                                time.sleep(2)
                                first_start = False
                            else:
                                self.noArm += 1

                        cTime = time.time()
                        fps = 1 / (cTime - pTime)
                        pTime = cTime
                        first_start = False
                        self.change_pixmap_signal.emit(img)

                    except:
                        pass
                else:
                    try:
                        point = crop(img)
                        warped = four_point_transform(img, point)
                        img = cv2.resize(warped, (int(600), int(700)),
                                         interpolation=cv2.INTER_CUBIC)
                        img = detector.findHands(img)
                        lmList = detector.findPosition(img, draw=False)
                        if len(lmList) != 0:
                            self.parkFlag = True
                            self.noArm = 0
                            id = 9
                            img = cv2.circle(img, (lmList[5][1], lmList[5][2]), radius=5, color=(100, 40, 40),
                                             thickness=-1)
                            img = cv2.circle(img, (lmList[17][1], lmList[17][2]), radius=5, color=(100, 40, 40),
                                             thickness=-1)
                            x = int(lmList[9][1]) * 2.5
                            y = int(lmList[9][2]) * 2.5
                            rxox = 300
                            rxoy = 0
                            trox = x
                            troy = y
                            try:
                                angle = math.atan((rxoy - troy) / (rxox - trox))
                            except:
                                angle = 90
                            x1 = rxox
                            x2 = trox
                            if x1 > x2:
                                angle += math.pi
                            angle = round(math.degrees(angle))
                            x_robot = -round(((math.fabs(math.sqrt((x - 600) ** 2 + (y - 0) ** 2))) / 40), 2)
                            x_robot += 0.02
                            f = 1233
                            w = 0.07
                            dis = math.sqrt(((lmList[5][1] - lmList[17][1]) * (lmList[5][1] - lmList[17][1])) + (
                                    (lmList[5][2] - lmList[17][2]) * (lmList[5][2] - lmList[17][2])))
                            dis2 = math.sqrt(((lmList[5][1] - lmList[8][1]) * (lmList[5][1] - lmList[8][1])) + (
                                    (lmList[5][2] - lmList[8][2]) * (lmList[5][2] - lmList[8][2])))
                            koef = (dis / twoo_dis)
                            z = (first_dis * koef)
                            try:
                                ang = (180 - (math.degrees(math.acos(dis2 / z)) + 80)) * 2
                                if ang < 75:
                                    ang = 20
                                elif ang < 140:
                                    ang = 90
                                else:
                                    ang = 165
                                telnet = telnetlib.Telnet('192.168.1.159')
                                s = f'D{ang}'
                                if self._record_start:
                                    self.new_script += f"{s} \n"
                                telnet.write(s.encode())
                                logger.info(s)
                                time.sleep(0.05)
                            except:
                                pass

                            y_robot = 90 - ((7 * f) / dis)
                            if y_robot >= -20 and y_robot <= 8:
                                if rotate_num > 145:
                                    y_robot = 0
                                else:
                                    y_robot = 8
                            elif y_robot >= 8 and y_robot <= 25:
                                y_robot = 17.5
                            elif y_robot >= 25 and y_robot <= 30:
                                y_robot = 27.5
                            else:
                                y_robot = 12.5
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

                            if self.tool == 'None':
                                pass
                            else:
                                if fingers[2] == 1:
                                    logger.info(f'Распознан поворот')
                                    str_send = 'F180'
                                    if self._record_start:
                                        self.new_script += f"{str_send} \n"
                                    telnet = telnetlib.Telnet('192.168.1.159')
                                    telnet.write(str_send.encode())
                                    logger.info(str_send)
                                    time.sleep(0.1)
                                    str_send = 'F90'
                                    if self._record_start:
                                        self.new_script += f"{str_send} \n"
                                    telnet = telnetlib.Telnet('192.168.1.159')
                                    telnet.write(str_send.encode())
                                    logger.info(str_send)
                                    time.sleep(0.1)
                                elif fingers[3] == 1:
                                    str_send = 'F0'
                                    if self._record_start:
                                        self.new_script += f"{str_send} \n"
                                    telnet = telnetlib.Telnet('192.168.1.159')
                                    telnet.write(str_send.encode())
                                    logger.info(str_send)
                                    time.sleep(0.1)
                                    str_send = 'F90'
                                    if self._record_start:
                                        self.new_script += f"{str_send} \n"
                                    telnet = telnetlib.Telnet('192.168.1.159')
                                    telnet.write(str_send.encode())
                                    logger.info(str_send)
                                    time.sleep(0.1)
                            cv2.putText(img, str(ang), (10, 70), cv2.FONT_HERSHEY_PLAIN,
                                        3, (255, 0, 0), 3)
                            cv2.putText(img, str(dis2), (10, 170), cv2.FONT_HERSHEY_PLAIN,
                                        3, (255, 0, 0), 3)

                            if angle < 180:
                                angle_ik = krest_trest.go_to([x_robot, y_robot], angle, flag_rotate)
                                logger.info(
                                    f'Передвижение в точку: {[x_robot, y_robot], angle, flag_rotate} Инструмент: {self.tool}')
                                a = angle_ik.split()
                                normal_ik = str()
                                angle_motor = a[1][1:]
                                for i in a[2:-1]:
                                    normal_ik += f"{str(i)} "

                                if self._record_start:
                                    self.new_script += f"{angle_ik} \n"
                        else:
                            if self.noArm >= 40 and self.parkFlag:
                                logger.info("Ушел в сон")
                                self.parkFlag = False
                                str_send = f"B60"
                                telnet = telnetlib.Telnet('192.168.1.159')
                                telnet.write(str_send.encode())
                                logger.info(str_send)
                                time.sleep(2)
                                str_send = 'C90'
                                telnet.write(str_send.encode())
                                logger.info(str_send)
                                time.sleep(2)
                                str_send = 'A90'
                                telnet.write(str_send.encode())
                                logger.info(str_send)
                                time.sleep(2)

                                str_send = 'D150 B55 C8'
                                telnet.write(str_send.encode())
                                logger.info(str_send)
                                time.sleep(2)
                                first_start = False
                            else:
                                self.noArm += 1

                        cTime = time.time()
                        fps = 1 / (cTime - pTime)
                        pTime = cTime
                        self.change_pixmap_signal.emit(img)

                    except:
                        pass
            else:
                pass
        cap.release()

    def stop(self):
        self._run_flag = False

    def start_(self):
        self._run_flag = True

    def parkFlafFalse(self):
        self.parkFlag = True
        self.noArm = 0

    def recordStart(self):
        self._record_start = True
        logger.info('Запись: старт')

    def recordEnd(self, tool):
        self._record_start = False
        self.name = str(random.randint(1, 1000000))
        print(self.new_script)
        conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
        cursor = conn.cursor()
        cursor.execute(f"insert into Scripts values (Null, '{self.name}', '{tool}ᅠ{self.new_script}', 'ang')")
        conn.commit()
        print(self.new_script)
        conn.close()
        self.new_script = ''
        logger.info('Запись: конец')
        return name


class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        uic.loadUi("G:/FingerTrackingInRealTime-main/main2.ui", self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("ARM63")
        self.disply_width = 640
        self.display_height = 480
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        self.image_label.move(20, 20)
        self.image_label.setStyleSheet("background-color: #C4C4C4")
        self.textLabel = QLabel('Webcam')
        self.thread = VideoThread()
        self.thread2 = AudioThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread2.check.connect(self.check)
        self.textEdit.textChanged.connect(self.scriptSave)
        self.scriptLoad()
        self.pushButton.clicked.connect(self.scriptStart)
        self.pushButton_2.clicked.connect(self.recordStart)
        self.pushButton_3.clicked.connect(self.recordEnd)
        self.pushButton_4.clicked.connect(self.goTo)
        self.pushButton_5.clicked.connect(self.toolBolt)
        self.pushButton_6.clicked.connect(self.toolZahvet)
        self.pushButton_7.clicked.connect(self.toolMarker)
        self.pushButton_8.clicked.connect(self.newScriptPoint)
        self.pushButton_10.clicked.connect(self.editScript)
        self.listWidget.itemSelectionChanged.connect(self.selectionChanged)
        self.thread.start()
        self.thread2.start()
        self.pushButton_3.hide()
        conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
        cursor = conn.cursor()
        cursor.execute(f'SELECT tool from info WHERE id = {1}')
        self.tool = cursor.fetchall()[0][0]
        conn.close()
        self.label_2.setText(self.tool)
        self.horizontalSlider.valueChanged.connect(self.horizontalSlider_changed)
        self.lineEdit_3.hide()
        self.lineEdit_4.hide()
        self.lineEdit_5.hide()
        self.pushButton_9.hide()
        self.pushButton_9.clicked.connect(self.addPoint)
        self.show()
        self.tool = None
        self.tool_new = None

    def newScriptPoint(self):
        self.pushButton_9.show()
        self.lineEdit_3.show()
        self.lineEdit_4.show()
        self.lineEdit_5.show()
        self._record_start = False
        if self.tool != None:
            tool = self.tool
        else:
            tool = 'Захват'
        self.name = str(random.randint(1, 1000000))
        conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
        cursor = conn.cursor()
        cursor.execute(f"insert into Scripts values (Null, '{self.name}', '{tool}ᅠ', 'point')")
        cursor.execute(f"SELECT id FROM Scripts WHERE name = '{self.name}'")
        self.id = cursor.fetchall()[0][0]
        cursor.execute(f"SELECT script FROM Scripts WHERE id = '{self.id}'")
        res = cursor.fetchall()[0][0]
        conn.commit()
        conn.close()
        self.textEdit.setPlainText(res)
        self.listWidget.clear()
        self.scriptLoad()
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')
        self.new_script = ''

    def addPoint(self):
        script = self.textEdit.toPlainText()
        script += f'{self.lineEdit_4.text()} {self.lineEdit_3.text()} {self.lineEdit_5.text()}\n '
        self.textEdit.setPlainText(script)

    def scriptSave(self):
        conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
        cursor = conn.cursor()
        print(1)
        cursor.execute(f"UPDATE Scripts SET script = '{self.textEdit.toPlainText()}' WHERE id = {self.id}")
        self.text = self.textEdit.toPlainText()
        conn.commit()

        conn.close()

    def editScript(self):
        conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
        cursor = conn.cursor()
        cursor.execute(f"SELECT type FROM Scripts WHERE id = '{self.id}'")
        res = cursor.fetchall()[0][0]
        conn.commit()
        conn.close()

        if res == 'point':
            self.pushButton_9.show()
            self.lineEdit_3.show()
            self.lineEdit_4.show()
            self.lineEdit_5.show()

    def selectionChanged(self):
        self.pushButton_9.hide()
        self.lineEdit_3.hide()
        self.lineEdit_4.hide()
        self.lineEdit_5.hide()
        self.textEdit.show()
        self.id, self.name = self.listWidget.currentItem().text().split("ᅠ")
        conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
        cursor = conn.cursor()
        cursor.execute(f'SELECT script from Scripts WHERE id = {self.id}')
        results = cursor.fetchall()
        sr = ''
        for i in results:
            sr += str(i[0])
        self.text = sr
        conn.close()
        self.noteUpdate()

    def noteUpdate(self):
        self.textEdit.setPlainText(self.text)

    def angle_update(self, angle_motor, ANGLE_IK):
        angle_ = []
        for i in ANGLE_IK.split():
            angle_.append(int(i[1:]))
        p = krest_trest.FK(angle_, [20, 19])
        self.m.new_plot(angle_motor, p)

    def toolBolt(self):
        self.tool_new = 'Болт'
        if self.tool_new != self.tool:
            self.toolChanger()
        else:
            self.tool_new = None
        self.label_2.setText(self.tool)
        conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE info SET tool = '{self.tool}' WHERE id = {1}")
        self.text = self.textEdit.toPlainText()
        conn.commit()
        conn.close()

    def toolZahvet(self):
        self.tool_new = 'Захват'
        if self.tool_new != self.tool:
            self.toolChanger()
        else:
            self.tool_new = None
        self.label_2.setText(self.tool)
        conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE info SET tool = '{self.tool}' WHERE id = {1}")
        self.text = self.textEdit.toPlainText()
        conn.commit()
        conn.close()

    def toolMarker(self):
        self.tool_new = 'Маркер'
        if self.tool_new != self.tool:
            self.toolChanger()
        else:
            self.tool_new = None
        self.label_2.setText(self.tool)
        conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE info SET tool = '{self.tool}' WHERE id = {1}")
        self.text = self.textEdit.toPlainText()
        conn.commit()
        conn.close()

    def toolChanger(self):
        print(self.tool)
        if self.tool is not None:
            if self.tool == 'Захват':
                logger.info('отдал завхат')
                self.thread.stop()
                conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
                cursor = conn.cursor()
                cursor.execute(f"SELECT script FROM Scripts WHERE id = 3")
                results = cursor.fetchall()
                print(results[0][0])
                for i in results[0][0].split('\n'):
                    str_send = f"{i}"
                    print(str_send)
                    telnet = telnetlib.Telnet('192.168.1.159')
                    telnet.write(str_send.encode())
                    time.sleep(2)
                conn.close()
                self.thread.start_()
            elif self.tool == 'Болт':
                logger.info('отдал Болт')
                self.thread.stop()
                conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
                cursor = conn.cursor()
                cursor.execute(f"SELECT script FROM Scripts WHERE id = 5")
                results = cursor.fetchall()
                print(results[0][0])
                for i in results[0][0].split('\n'):
                    str_send = f"{i}"
                    print(str_send)
                    telnet = telnetlib.Telnet('192.168.1.159')
                    telnet.write(str_send.encode())
                    time.sleep(2)
                conn.close()
                self.thread.start_()
            elif self.tool == 'Маркер':
                logger.info('отдал Маркер')
                self.thread.stop()
                conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
                cursor = conn.cursor()
                cursor.execute(f"SELECT script FROM Scripts WHERE id = 11")
                results = cursor.fetchall()
                print(results[0][0])
                for i in results[0][0].split('\n'):
                    str_send = f"{i}"
                    telnet = telnetlib.Telnet('192.168.1.159')
                    telnet.write(str_send.encode())
                    time.sleep(2)
                conn.close()
                self.thread.start_()

            if self.tool_new == 'Захват':
                logger.info('взял захват')
                self.thread.stop()
                conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
                cursor = conn.cursor()
                cursor.execute(f"SELECT script FROM Scripts WHERE id = 1")
                results = cursor.fetchall()
                for i in results[0][0].split('\n'):
                    str_send = f"{i}"
                    telnet = telnetlib.Telnet('192.168.1.159')
                    telnet.write(str_send.encode())
                    time.sleep(2)
                conn.close()
                self.thread.start_()
                self.tool = self.tool_new
                self.tool_new = None
            elif self.tool_new == 'Болт':
                logger.info('взял Болт')
                self.thread.stop()
                conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
                cursor = conn.cursor()
                cursor.execute(f"SELECT script FROM Scripts WHERE id = 4")
                results = cursor.fetchall()
                for i in results[0][0].split('\n'):
                    print(i)
                    str_send = f"{i}"
                    telnet = telnetlib.Telnet('192.168.1.159')
                    telnet.write(str_send.encode())
                    time.sleep(2)
                conn.close()
                self.tool = self.tool_new
                self.tool_new = None
                self.thread.start_()
            elif self.tool_new == 'Маркер':
                logger.info('взял Маркер')
                self.thread.stop()
                conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
                cursor = conn.cursor()
                cursor.execute(f"SELECT script FROM Scripts WHERE id = 10")
                results = cursor.fetchall()
                for i in results[0][0].split('\n'):
                    str_send = f"{i}"
                    telnet = telnetlib.Telnet('192.168.1.159')
                    telnet.write(str_send.encode())
                    time.sleep(2)
                conn.close()
                self.tool = self.tool_new
                self.tool_new = None
                self.thread.start_()
        else:
            if self.tool_new == 'Захват':
                logger.info('взял захват')
                self.thread.stop()
                conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
                cursor = conn.cursor()
                cursor.execute(f"SELECT script FROM Scripts WHERE id = 1")
                results = cursor.fetchall()
                for i in results[0][0].split('\n'):
                    str_send = f"{i}"
                    telnet = telnetlib.Telnet('192.168.1.159')
                    telnet.write(str_send.encode())
                    time.sleep(2)
                conn.close()
                self.thread.start_()
                self.tool = self.tool_new
                self.tool_new = None
            elif self.tool_new == 'Болт':
                logger.info('взял Болт')
                self.thread.stop()
                conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
                cursor = conn.cursor()
                cursor.execute(f"SELECT script FROM Scripts WHERE id = 4")
                results = cursor.fetchall()
                for i in results[0][0].split('\n'):
                    str_send = f"{i}"
                    telnet = telnetlib.Telnet('192.168.1.159')
                    telnet.write(str_send.encode())
                    time.sleep(2)
                conn.close()
                self.tool = self.tool_new
                self.tool_new = None
                self.thread.start_()
            elif self.tool_new == 'Маркер':
                logger.info('взял Маркер')
                self.thread.stop()
                conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
                cursor = conn.cursor()
                cursor.execute(f"SELECT script FROM Scripts WHERE id = 10")
                results = cursor.fetchall()
                for i in results[0][0].split('\n'):
                    str_send = f"{i}"
                    telnet = telnetlib.Telnet('192.168.1.159')
                    telnet.write(str_send.encode())
                    time.sleep(2)
                conn.close()
                self.tool = self.tool_new
                self.tool_new = None
                self.thread.start_()
        self.thread.parkFlafFalse()

    def goTo(self):
        x_robot = float(self.lineEdit.text()) * -1
        y_robot = float(self.lineEdit_2.text())
        angle_ik = krest_trest.go_to([x_robot, y_robot], 90, True)
        logger.info(f'Передвижение в точку: {[x_robot, y_robot], 90, True} Инструмент: {self.tool}')
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.thread.parkFlafFalse()

    def horizontalSlider_changed(self):
        self.label.setText(str(self.horizontalSlider.value()))
        str_new = f'A{self.horizontalSlider.value()}'
        logger.info(f'A{self.horizontalSlider.value()}')
        telnet = telnetlib.Telnet('192.168.1.159')
        telnet.write(str_new.encode())
        time.sleep(0.2)

    def scriptLoad(self):
        conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM Scripts")
        results = cursor.fetchall()
        id_official = [1, 2, 4, 10]
        for i in results:
            if not int(i[0]) in id_official:
                self.listWidget.addItem(f"{str(i[0])}ᅠ{str(i[1])}")
        conn.close()

    def recordStart(self):
        self.thread.recordStart()
        self.pushButton_3.show()

    def scriptStart(self):
        self.thread.stop()
        conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
        cursor = conn.cursor()
        item = self.listWidget.currentItem()
        if item is not None:
            cursor.execute(f"SELECT script, type FROM Scripts WHERE id = {item.text().split('ᅠ')[0]}")
            results = cursor.fetchall()
            scrii = results[0][0]
            if results[0][1] == 'ang':
                try:
                    tool_new1 = results[0][0].split("ᅠ")[0]
                    if tool_new1 == 'Захват' and self.tool != 'Захват':
                        self.toolZahvet()
                    elif tool_new1 == 'Болт' and self.tool != 'Болт':
                        self.toolBolt()
                    elif tool_new1 == 'Маркер' and self.tool != 'Маркер':
                        self.toolBolt()
                        scrii = results[0][0].split("ᅠ")[1]
                except:
                    pass

                for i in scrii.split('\n'):
                    try:
                        str_send = f"{i}"
                        print(str_send)
                        if str_send[0] == 'F':
                            telnet = telnetlib.Telnet('192.168.1.159')
                            telnet.write(str_send.encode())
                            logger.info(str_send)
                            time.sleep(0.1)
                        else:
                            telnet = telnetlib.Telnet('192.168.1.159')
                            telnet.write(str_send.encode())
                            time.sleep(0.08)
                    except:
                        pass
            else:
                tool_new1 = results[0][0].split("ᅠ")[0]
                scrii = results[0][0].split("ᅠ")[1]
                for i in scrii.split('\n'):
                    try:
                        x, y, z = i.split()
                        x = int(x)
                        y = int(y)
                        z = int(z)
                        rxox = 30
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
                        x_robot = -round(((math.fabs(math.sqrt((trox - 60) ** 2 + (troy - 0) ** 2))) / 4), 2)
                        x_robot += 0.02
                        y_robot = z
                        # y_robot = float(self.lineEdit_5.text())
                        angle_ik = krest_trest.go_to([x_robot, y_robot], angle, True)
                        logger.info(
                            f'Передвижение в точку: {[x_robot, y_robot]}, {angle}, {True} Инструмент: {self.tool}')
                        time.sleep(1)
                    except:
                        pass

                conn.close()
        time.sleep(1)
        self.thread.start_()
        self.thread.parkFlafFalse()

    def recordEnd(self):
        self.thread.recordEnd(self.tool)
        self.pushButton_3.hide()
        self.listWidget.clear()
        self.scriptLoad()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    @pyqtSlot(str)
    def check(self, text):
        if text == 'Взял захват':
            if self.tool != 'Захват':
                print('Взял захват')
                self.toolZahvet()
        elif text == 'Взял болт':
            if self.tool != 'Болт':
                print('Взял болт')
                self.toolBolt()
                print('Прошел')
        elif text == 'Взял маркер':
            if self.tool != 'Маркер':
                self.toolMarker()

        elif text == 'Болт20':
            if self.tool != 'Болт':
                self.toolBolt()
            self.thread.stop()
            conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
            cursor = conn.cursor()
            item = True
            if item is not None:
                cursor.execute(f"SELECT script, type FROM Scripts WHERE id = 25")
                results = cursor.fetchall()
                scrii = results[0][0]
                try:
                    scrii = results[0][0].split("ᅠ")[1]
                except:
                    print(scrii)

                print(scrii)
                for i in scrii.split('\n'):
                    str_send = f"{i}"
                    print(i)
                    if str_send[0] == 'F':
                        print(str_send)
                        telnet = telnetlib.Telnet('192.168.1.159')
                        telnet.write(str_send.encode())
                        logger.info(str_send)
                        time.sleep(0.1)
                    else:
                        print(str_send)
                        telnet = telnetlib.Telnet('192.168.1.159')
                        telnet.write(str_send.encode())
                        logger.info(str_send)
                        time.sleep(2)
        elif text == 'Болт20У':
            if self.tool == 'Болт':
                self.toolBolt()
                self.thread.stop()
                conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
                cursor = conn.cursor()
                item = True
                if item is not None:
                    print(20)
                    cursor.execute(f"SELECT script, type FROM Scripts WHERE id = 26")
                    results = cursor.fetchall()
                    scrii = results[0][0]
                    try:
                        scrii = results[0][0].split("ᅠ")[1]
                    except:
                        print(scrii)

                    print(scrii)
                    for i in scrii.split('\n'):
                        str_send = f"{i}"
                        print(i)
                        if str_send[0] == 'F':
                            print(str_send)
                            telnet = telnetlib.Telnet('192.168.1.159')
                            telnet.write(str_send.encode())
                            logger.info(str_send)
                            time.sleep(0.1)
                        else:
                            print(str_send)
                            telnet = telnetlib.Telnet('192.168.1.159')
                            telnet.write(str_send.encode())
                            logger.info(str_send)
                            time.sleep(2)
        elif text == 'Протирка':
            if 1 < 2:
                self.thread.stop()
                conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
                cursor = conn.cursor()
                item = True
                if item is not None:
                    cursor.execute(f"SELECT script, type FROM Scripts WHERE id = 39")
                    results = cursor.fetchall()
                    scrii = results[0][0]
                    try:
                        scrii = results[0][0].split("ᅠ")[1]
                    except:
                        print(scrii)

                    print(scrii)
                    for i in scrii.split('\n'):
                        str_send = f"{i}"
                        print(i)
                        if str_send[0] == 'F':
                            print(str_send)
                            telnet = telnetlib.Telnet('192.168.1.159')
                            telnet.write(str_send.encode())
                            logger.info(str_send)
                            time.sleep(0.1)
                        else:
                            print(str_send)
                            telnet = telnetlib.Telnet('192.168.1.159')
                            telnet.write(str_send.encode())
                            logger.info(str_send)
                            time.sleep(2)
        elif text == 'Рисую':
            if 1 < 2:
                self.thread.stop()
                conn = sqlite3.connect('G:/FingerTrackingInRealTime-main/db/main.sqlite3')
                cursor = conn.cursor()
                item = True
                if item is not None:
                    cursor.execute(f"SELECT script, type FROM Scripts WHERE id = 40")
                    results = cursor.fetchall()
                    scrii = results[0][0]
                    try:
                        scrii = results[0][0].split("ᅠ")[1]
                    except:
                        print(scrii)

                    print(scrii)
                    for i in scrii.split('\n'):
                        str_send = f"{i}"
                        print(i)
                        if str_send[0] == 'F':
                            print(str_send)
                            telnet = telnetlib.Telnet('192.168.1.159')
                            telnet.write(str_send.encode())
                            logger.info(str_send)
                            time.sleep(0.2)
                        else:
                            print(str_send)
                            telnet = telnetlib.Telnet('192.168.1.159')
                            telnet.write(str_send.encode())
                            logger.info(str_send)
                            time.sleep(2)
        self.thread.start_()
        self.thread.parkFlafFalse()

    def textNew(self, func):
        print(func)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
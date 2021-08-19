import time
import cv2
import HandTrackingModule as htm
import numpy as np
import random
from util3d import runtime_init, draw_line, draw_ball, draw_dot, draw_cuboid
from interaction import *
from gen3d import gen3d, trace3d
from math import floor
from queue import Queue
from threading import Thread
import azure.cognitiveservices.speech as speechsdk
import matplotlib.pyplot as plt


class Painter:
    def __init__(self, opt: Options):
        # Display function init
        self.plain = np.zeros((480, 640, 3), np.uint8)           # plots
        self.panel = np.zeros((480, 640, 3), np.uint8)           # bottoms
        self.img = np.zeros((480, 640, 3), np.uint8)                # img
        self.result = np.zeros((480, 640, 3), np.uint8)
        self.show_zone = [0, 0]                                  # the display area
        self.absolute_coor = [0, 0]                              # the absolute coordinate of the paint
        self.ax = runtime_init()

        # painting init
        self.pre_dot = (0, 0, 0)
        self.begin_dot = (0, 0, 0)
        self.center = (0, 0, 0)
        self.color = (255, 255, 0)
        self.draw_mode = 'cuboid'
        self.Signature = "H.Chen"
        self.save_timestamp, self.switch_timestamp, self.text_timestamp, \
        self.line_timestamp, self.move_timestamp, self.voice_timestamp = 0, 0, 0, 0, 0, 0
        self.radius = 5

        # hand detectors
        self.detector = htm.handDetctor(detectionCon=0.7)

        self.project_name = project_init()
        self.file = None

        # Options
        self.opt = opt
        self.opt.preview3d = False
        self.opt.view3d = False
        self.opt.export3d = False

        wCam, hCam = 640, 480
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(3, wCam)
        self.cap.set(4, hCam)

        self.request_queue = Queue()
        self.result_queue = Queue()
        self.killed = False

    def display_init(self):
        cv2.rectangle(self.panel, (520, 0), (640, 40), (255, 99, 93), -1)
        cv2.rectangle(self.panel, (520, 440), (640, 480), (255, 99, 93), -1)
        cv2.rectangle(self.panel, (0, 440), (120, 480), (255, 99, 93), -1)
        if time.time()-self.switch_timestamp > 5:
            cv2.rectangle(self.panel, (0, 0), (120, 40), (255, 99, 93), -1)
        else:
            cv2.rectangle(self.panel, (0, 0), (120, 40), (135, 62, 57), -1)
        cv2.putText(self.panel, "Clear", (530, 20), cv2.FONT_HERSHEY_PLAIN, 1, (46, 255, 224), 1)
        cv2.putText(self.panel, "Save", (10, 460), cv2.FONT_HERSHEY_PLAIN, 1, (46, 255, 224), 1)
        cv2.putText(self.panel, "Exit", (530, 460), cv2.FONT_HERSHEY_PLAIN, 1, (46, 255, 224), 1)
        cv2.putText(self.panel, self.draw_mode + " mode", (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (46, 255, 224), 1)
        if self.draw_mode == 'move':
            cv2.rectangle(self.panel, (160, 0), (480, 40), (116, 153, 255), -1)
            cv2.putText(self.panel, "L", (200, 20), cv2.FONT_HERSHEY_PLAIN, 1, (46, 255, 224), 1)
            cv2.putText(self.panel, "T", (280, 20), cv2.FONT_HERSHEY_PLAIN, 1, (46, 255, 224), 1)
            cv2.putText(self.panel, "B", (360, 20), cv2.FONT_HERSHEY_PLAIN, 1, (46, 255, 224), 1)
            cv2.putText(self.panel, "R", (440, 20), cv2.FONT_HERSHEY_PLAIN, 1, (46, 255, 224), 1)
        else:
            cv2.rectangle(self.panel, (160, 0), (480, 40), (0, 0, 0), -1)

    def painter_exit(self):
        self.file.close()
        self.killed = True
        import shutil
        shutil.copy('trace.txt', './output/{}/trace.txt'.format(self.project_name))
        if self.opt.export3d or self.opt.view3d:
            gen3d()
        if self.opt.view3d_trace:
            trace3d()
        exit()

    def clear(self):
        self.plain = np.zeros((480, 640, 3), np.uint8)
        plt.cla()
        self.show_zone = [0, 0]
        self.file.write("clear\n")
        self.pre_dot = (0, 0, 0)
        self.center = (0, 0, 0)

    def on_EVENT_LBUTTONDOWN(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if x > 520 and y < 40:
                self.clear()
            elif x < 120 and y < 40:
                self.draw_mode = switch_mode(self.draw_mode)
            elif x > 520 and y > 440:
                self.painter_exit()
            elif x < 120 and y > 440:
                self.save_photo()
                self.save_timestamp = time.time()
                cv2.rectangle(self.img, (0, 440), (120, 480), (0, 0, 0), -1)

    def move_panel(self, image, x=None, direction_str: str=None):
        if time.time() - self.move_timestamp < 0.5:
            return image
        self.move_timestamp = time.time()
        direction = floor((x - 160) / 80)
        self.file.write("move\n")
        if direction == 1 or direction_str == 'top':              # Top
            self.absolute_coor[1] -= 50
            if self.show_zone[1] == 0:
                image = cv2.copyMakeBorder(image, 50, 0, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
            else:
                self.show_zone[1] -= 50

        elif direction == 2 or direction_str == 'down':
            self.absolute_coor[1] += 50
            if self.show_zone[1] + 480 == image.shape[0]:
                image = cv2.copyMakeBorder(image, 0, 50, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
            self.show_zone[1] += 50

        elif direction == 0 or direction_str == 'left':
            self.absolute_coor[0] -= 50
            if self.show_zone[0] == 0:
                image = cv2.copyMakeBorder(image, 0, 0, 50, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
            else:
                self.show_zone[0] -= 50

        elif direction == 3 or direction_str == 'right':
            self.absolute_coor[0] += 50
            if self.show_zone[0] + 640 == image.shape[1]:
                image = cv2.copyMakeBorder(image, 0, 0, 0, 50, cv2.BORDER_CONSTANT, value=(0, 0, 0))
            self.show_zone[0] += 50
        return image

    def save_photo(self):
        now = datetime.datetime.now()
        cv2.imwrite("./output/{}/Image{}.jpg".format(self.project_name, now.strftime("%M_%S")), self.result)

    def speech_recognition(self):
        try:
            azure_license = open("azure_key.txt")
            key, region = azure_license.readline()[:-1].split()
            print("Using sdk from ", region)
            speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
            speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
            while not self.killed:
                if not self.request_queue.empty():
                    self.request_queue.get()
                    result = speech_recognizer.recognize_once_async().get()
                    # print(result.text)
                    self.result_queue.put(result.text)
        except FileNotFoundError as e:
            print(e)
            print('Please check out voice control wiki at\n'
                  'https://github.com/HarryXD2018/3DPainter/wiki/Installation#voice-control-service')


    def run(self):
        with open('trace.txt', 'w') as f:
            self.file = f
            f.write(self.project_name + '\n')          # 1 is meaningless but to make gen works.
            while True:
                success, self.img = self.cap.read()
                self.img = cv2.flip(self.img, 1)
                self.img = self.detector.findHands(self.img)
                lmList = self.detector.findPosition(self.img, draw=False)
                self.display_init()
                if not self.result_queue.empty():
                    command: str = self.result_queue.get()
                    command = command.lower()
                    print(command)
                    if 'exit' in command:
                        self.painter_exit()
                    elif 'clear' in command:
                        self.clear()
                    elif 'mode' in command:
                        for mode in ['brush', 'ball', 'dot', 'line', 'cuboid', 'text']:
                            if mode in command:
                                self.draw_mode = mode
                    for direction in ['top', 'down', 'left', 'right']:
                        if direction in command:
                            self.plain = self.move_panel(self.plain, direction_str=direction)
                if len(lmList) != 0:
                    thumbOpen, firstOpen, secondOpen, thirdOpen, fourthOpen = self.detector.fingerStatus(lmList)
                    if firstOpen and not secondOpen and not thirdOpen and not fourthOpen:
                        _, screen_x, screen_y, z = lmList[8]
                        absolute_x, absolute_y = coor3d((screen_x, screen_y), self.absolute_coor)
                        plain_x, plain_y = img2plain(screen_x, screen_y, self.show_zone)
                        # Move
                        if self.draw_mode == 'move':
                            if 160 < screen_x < 480 and screen_y < 40:
                                self.plain = self.move_panel(self.plain, x=screen_x)

                        # Switch Mode
                        if screen_x < 120 and screen_y < 40 and time.time()-switch_timestamp > 10:
                            switch_timestamp = time.time()
                            self.draw_mode = switch_mode(self.draw_mode)
                            self.pre_dot = (0, 0, 0)

                        # Clear Plain
                        elif screen_x > 360 and screen_y < 40:
                            self.clear()

                        else:
                            if self.draw_mode == 'brush':
                                if self.pre_dot != (0, 0, 0):
                                    cv2.line(self.plain, (plain_x, plain_y), self.pre_dot[:2], self.color, 3)
                                    draw_line(self.ax, (absolute_x, absolute_y, z),
                                              plain2abs(self.pre_dot, coor=self.absolute_coor, zone=self.show_zone), color=self.color)
                                    f.write("b {} {} {} {} {} {}\n".format(absolute_x, absolute_y, z,
                                                                           self.color[2], self.color[1], self.color[0]))
                                self.pre_dot = (plain_x, plain_y, z)

                            elif self.draw_mode == 'ball':
                                if self.center != (0, 0, 0):
                                    cv2.circle(self.plain, center=self.center[:2],
                                               color=(0, 255, 255), radius=self.radius, thickness=-1)
                                    draw_ball(self.ax, plain2abs(self.center, coor=self.absolute_coor, zone=self.show_zone), self.radius)
                                    str_temp = list(map(str, plain2abs(self.center, coor=self.absolute_coor, zone=self.show_zone)))
                                    str_temp = " ".join(str_temp)
                                    self.file.write("s " + str_temp + " {}\n".format(self.radius))
                                    self.center = (0, 0, 0)
                                    self.radius = 5

                            elif self.draw_mode == 'line':
                                if self.begin_dot != (0, 0, 0):
                                    cv2.line(self.img, (screen_x, screen_y),
                                             plain2img(self.begin_dot[0], self.begin_dot[1], self.show_zone),
                                             (205, 0, 255), 3)

                            elif self.draw_mode == 'cuboid':
                                if self.begin_dot != (0, 0, 0):
                                    cv2.rectangle(self.img, (screen_x, screen_y),
                                                  plain2img(self.begin_dot[0], self.begin_dot[1], self.show_zone),
                                                  (245, 255, 79), 3)

                            elif self.draw_mode == 'dot':
                                self.pre_dot = (plain_x, plain_y, z)

                    # Eraser
                    if firstOpen and secondOpen and not thirdOpen and not fourthOpen:
                        _, screen_x, screen_y, z = lmList[8]
                        plain_x, plain_y = img2plain(screen_x, screen_y, self.show_zone)
                        cv2.rectangle(self.plain, (plain_x-15, plain_y-15), (plain_x+15, plain_y+15), (0, 0, 0), -1)
                        cv2.rectangle(self.img, (screen_x - 15, screen_y - 15), (screen_x + 15, screen_y + 15), (255, 255, 255), -1)
                        cv2.rectangle(self.img, (screen_x - 15, screen_y - 15), (screen_x + 15, screen_y + 15), (0, 0, 0), 1)
                        self.pre_dot = (0, 0, 0)

                    if firstOpen and fourthOpen and not secondOpen and not thirdOpen:
                        _, screen_x, screen_y, z = lmList[8]
                        absolute_x, absolute_y = coor3d((screen_x, screen_y), self.absolute_coor)
                        plain_x, plain_y = img2plain(screen_x, screen_y, self.show_zone)
                        if self.draw_mode == 'brush':
                            self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

                        # Template, don't draw on img
                        elif self.draw_mode == 'ball':
                            self.center = (plain_x, plain_y, z)
                            cv2.circle(self.img, center=(screen_x, screen_y), color=(0, 200, 200), radius=self.radius, thickness=3)
                            if int(time.time()) % 2 == 0:
                                self.radius += 5

                        elif self.draw_mode == 'dot':
                            cv2.circle(self.plain, center=(plain_x, plain_y), color=(0, 255, 35), radius=2, thickness=-1)
                            draw_dot(self.ax, (absolute_x, absolute_y, z))
                            str_temp = list(map(str, plain2abs(self.pre_dot, self.absolute_coor, self.show_zone)))
                            self.file.write("d " + " ".join(str_temp) + " \n")

                        elif self.draw_mode == 'line':
                            if self.begin_dot == (0, 0, 0):
                                if time.time()-self.line_timestamp > 2:
                                    self.begin_dot = (plain_x, plain_y, z)
                            elif abs(self.begin_dot[0] - plain_x) + abs(self.begin_dot[1] - plain_y) > 20:
                                cv2.line(self.plain, (plain_x, plain_y), self.begin_dot[:2], (205, 0, 255), 3)
                                draw_line(self.ax, (absolute_x, absolute_y, z),
                                          plain2abs(self.begin_dot, self.absolute_coor, self.show_zone), (205, 0, 255))
                                str_temp = list(map(str, plain2abs(self.begin_dot, self.absolute_coor, self.show_zone)))
                                self.file.write("l {} {} {} ".format(absolute_x, absolute_y, z) + " ".join(str_temp) + "\n")
                                self.begin_dot = (0, 0, 0)
                                self.line_timestamp = time.time()

                        elif self.draw_mode == 'cuboid':
                            if self.begin_dot == (0, 0, 0):
                                if time.time()-self.line_timestamp > 2:
                                    self.begin_dot = (plain_x, plain_y, z)
                            elif abs(self.begin_dot[0] - plain_x) + abs(self.begin_dot[1] - plain_y) > 20:
                                cv2.rectangle(self.plain, (plain_x, plain_y), self.begin_dot[:2], (245, 255, 79), -1)
                                draw_cuboid(self.ax, (absolute_x, absolute_y, z),
                                            plain2abs(self.begin_dot, self.absolute_coor, self.show_zone), (245, 255, 79))
                                str_temp = list(map(str, plain2abs(self.begin_dot, self.absolute_coor, self.show_zone)))
                                self.file.write("c {} {} {} ".format(plain_x, plain_y, z) + " ".join(str_temp) + " \n")
                                self.begin_dot = (0, 0, 0)
                                self.line_timestamp = time.time()

                        elif self.draw_mode == 'text':
                            if time.time()-self.text_timestamp > 2:
                                cv2.putText(self.plain, self.Signature, (plain_x, plain_y), cv2.FONT_HERSHEY_PLAIN, 3, (102, 248, 255), 1)
                                self.file.write("t {} {} {} {}\n".format(absolute_x, absolute_y, z, self.Signature))
                                self.text_timestamp = time.time()
                    if not firstOpen:
                        self.pre_dot = (0, 0, 0)
                        self.center = (0, 0, 0)

                    if firstOpen and secondOpen and thumbOpen and thirdOpen and fourthOpen:
                        if time.time() - self.voice_timestamp > 10:
                            self.request_queue.put(1)
                            self.voice_timestamp = time.time()
                        else:
                            cv2.circle(self.img, center=(320, 30), color=(0, 0, 255), radius=15, thickness=-1)
                            cv2.circle(self.img, center=(320, 30), color=(0, 0, 255), radius=25, thickness=2)

                temp = self.plain[self.show_zone[1]: (self.show_zone[1]+480), self.show_zone[0]: (self.show_zone[0]+640)]
                cv2.imshow("full view", self.plain)

                if time.time() - self.save_timestamp < 0.4:          # camera shooter effect
                    self.img = cv2.add(self.img, self.img)

                self.result = cv2.addWeighted(self.img, 0.7, temp, 0.3, 0)
                img2gray = cv2.cvtColor(self.panel, cv2.COLOR_BGR2GRAY)
                ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
                mask_inv = cv2.bitwise_not(mask)
                img1_bg = cv2.bitwise_and(self.result, self.result, mask=mask_inv)
                display = cv2.add(img1_bg, self.panel)
                cv2.imshow("image", display)
                cv2.setMouseCallback("image", self.on_EVENT_LBUTTONDOWN)
                if self.opt.preview3d:
                    plt.pause(0.1)
                if cv2.waitKey(2) & 0xFF == 27:
                    plt.ioff()
                    break


if __name__ == '__main__':
    opt.view3d_trace = False
    opt.export3d = False
    opt.preview3d = True
    painter = Painter(opt)
    main_thread = Thread(target=painter.run)
    voice_thread = Thread(target=painter.speech_recognition, daemon=True)
    main_thread.start()
    voice_thread.start()

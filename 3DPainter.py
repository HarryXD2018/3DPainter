import time
import cv2
import os
import HandTrackingModule as htm
import numpy as np
import random
from util3d import runtime_init, draw_line, MODE3D, draw_ball
from interaction import switch_mode

import matplotlib.pyplot as plt


def display_init():
    cv2.rectangle(img, (520, 0), (640, 40), (255, 99, 93), -1)
    cv2.rectangle(img, (520, 440), (640, 480), (255, 99, 93), -1)
    if time.time()-switch_timestamp > 5:
        cv2.rectangle(img, (0, 0), (120, 40), (255, 99, 93), -1)
    else:
        cv2.rectangle(img, (0, 0), (120, 40), (135, 62, 57), -1)
    cv2.putText(img, "Clear", (530, 20), cv2.FONT_HERSHEY_PLAIN, 1, (46, 255, 224), 1)
    cv2.putText(img, "Exit", (530, 460), cv2.FONT_HERSHEY_PLAIN, 1, (46, 255, 224), 1)
    cv2.putText(img, draw_mode + " mode", (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (46, 255, 224), 1)


def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    global plain
    global pre_dot
    global center
    global draw_mode
    if event == cv2.EVENT_LBUTTONDOWN:
        if x > 520 and y < 40:
            plain = np.zeros((480, 640, 3), np.uint8)
            plt.cla()
            pre_dot = (0, 0, 0)
            center = (0, 0, 0)
        elif x < 120 and y < 40:
            draw_mode = switch_mode(draw_mode)
        elif x > 520 and y > 440:
            exit()


wCam, hCam = 640, 480
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, wCam)
cap.set(4, hCam)


if __name__ == '__main__':
    plain = np.zeros((480, 640, 3), np.uint8)
    pre_dot = (0, 0, 0)
    center = (0, 0, 0)
    color = (255, 255, 0)
    detector = htm.handDetctor(detectionCon=0.7)
    ax = runtime_init()
    draw_mode = 'pencil'
    MODE3D = True
    switch_timestamp = 0
    radius = 5
    with open('trace.txt', 'w') as f:
        while True:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            img = detector.findHands(img)
            lmList = detector.findPosition(img, draw=False)
            display_init()
            if len(lmList) != 0:
                thumbOpen, firstOpen, secondOpen, thirdOpen, fourthOpen = detector.fingerStatus(lmList)
                if firstOpen and not secondOpen and not thirdOpen and not fourthOpen:
                    _, x, y, z = lmList[8]
                    # cv2.putText(img, "{}".format(z), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

                    # Switch Mode
                    if x < 120 and y < 40 and time.time()-switch_timestamp > 10:
                        switch_timestamp = time.time()
                        draw_mode = switch_mode(draw_mode)
                        pre_dot = (0, 0, 0)

                    # Clear Plain
                    if x > 360 and y < 40:
                        plain = np.zeros((480, 640, 3), np.uint8)
                        plt.cla()
                        pre_dot = (0, 0, 0)
                        center = (0, 0, 0)

                    elif draw_mode == 'pencil':
                        if pre_dot != (0, 0, 0):
                            cv2.line(plain, (x, y), pre_dot[:2], color, 3)
                            draw_line(ax, (x, y, z), pre_dot)
                            f.write("{} {} {}\n".format(x, y, z))
                        pre_dot = (x, y, z)
                        if random.random() > 0.5:
                            print(pre_dot)
                    elif draw_mode == 'ball':
                        if center != (0, 0, 0):
                            print(center, radius)
                            cv2.circle(plain, center=center[:2], color=(0, 255, 255), radius=radius, thickness=3)
                            draw_ball(ax, center, radius)
                            center = (0, 0, 0)
                            radius = 5

                if firstOpen and secondOpen and not thirdOpen and not fourthOpen:
                    _, x, y, z = lmList[8]
                    cv2.circle(plain, center=(x, y), color=(0, 0, 0), radius=15, thickness=-1)
                    cv2.rectangle(img, (x-15, y-15), (x+15, y+15), (255, 255, 255), -1)
                    cv2.rectangle(img, (x-15, y-15), (x+15, y+15), (0, 0, 0), 1)
                    # cv2.circle(img, center=(x, y), color=(255, 255, 0), radius=15, thickness=-1)
                    pre_dot = (0, 0, 0)
                # if not firstOpen and not secondOpen and not thirdOpen and not fourthOpen:       # Rock
                    # cv2.putText(img, "Rock", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                # if firstOpen and secondOpen and not thirdOpen and not fourthOpen:               # Scissors
                #     cv2.putText(img, "Scissors", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                # if firstOpen and secondOpen and thirdOpen and fourthOpen:
                #     # cv2.putText(img, "Paper", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                #     plain = np.zeros((480, 640, 3), np.uint8)
                #     if MODE3D:
                #         plt.cla()
                #     pre_dot = (0, 0, 0)
                if firstOpen and fourthOpen and not secondOpen and not thirdOpen:
                    if draw_mode == 'pencil':
                        color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
                    elif draw_mode == 'ball':
                        center = (x, y, z)
                        cv2.circle(img, center=center[:2], color=(0, 200, 200), radius=radius, thickness=3)
                        if int(time.time()) % 2 == 0:
                            radius += 5
                if not firstOpen:
                    pre_dot = (0, 0, 0)
                    center = (0, 0, 0)
            result = cv2.addWeighted(img, 0.7, plain, 0.3, 0)
            cv2.imshow("image", result)
            cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
            if MODE3D:
                plt.pause(0.1)
            if cv2.waitKey(2) & 0xFF == 27:
                plt.ioff()
                break


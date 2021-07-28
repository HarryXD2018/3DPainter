import time, datetime
import cv2
import HandTrackingModule as htm
import numpy as np
import random
from util3d import runtime_init, draw_line, MODE3D, draw_ball, draw_dot, draw_cuboid
from interaction import switch_mode
from gen3d import gen3d

import matplotlib.pyplot as plt


def display_init():
    cv2.rectangle(panel, (520, 0), (640, 40), (255, 99, 93), -1)
    cv2.rectangle(panel, (520, 440), (640, 480), (255, 99, 93), -1)
    cv2.rectangle(panel, (0, 440), (120, 480), (255, 99, 93), -1)
    if time.time()-switch_timestamp > 5:
        cv2.rectangle(panel, (0, 0), (120, 40), (255, 99, 93), -1)
    else:
        cv2.rectangle(panel, (0, 0), (120, 40), (135, 62, 57), -1)
    cv2.putText(panel, "Clear", (530, 20), cv2.FONT_HERSHEY_PLAIN, 1, (46, 255, 224), 1)
    cv2.putText(panel, "Save", (10, 460), cv2.FONT_HERSHEY_PLAIN, 1, (46, 255, 224), 1)
    cv2.putText(panel, "Exit", (530, 460), cv2.FONT_HERSHEY_PLAIN, 1, (46, 255, 224), 1)
    cv2.putText(panel, draw_mode + " mode", (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (46, 255, 224), 1)


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
            f.close()
            if GEN3D:
                gen3d()
            exit()
        elif x < 120 and y > 440:
            save_photo()
            cv2.rectangle(img, (0, 440), (120, 480), (0, 0, 0), -1)


def save_photo():
    now = datetime.datetime.now()
    cv2.imwrite("./output/Image{}.jpg".format(now.strftime("%Y%m%d%H%M%S")), result)


wCam, hCam = 640, 480
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, wCam)
cap.set(4, hCam)


if __name__ == '__main__':
    # Display function init
    plain = np.zeros((480, 640, 3), np.uint8)
    panel = np.zeros((480, 640, 3), np.uint8)
    ax = runtime_init()

    # painting init
    pre_dot = (0, 0, 0)
    begin_dot = (0, 0, 0)
    center = (0, 0, 0)
    color = (255, 255, 0)
    draw_mode = 'brush'
    MODE3D = True
    GEN3D = True
    switch_timestamp = 0
    line_timestamp = 0
    radius = 5

    # hand detectors
    detector = htm.handDetctor(detectionCon=0.7)

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

                    elif draw_mode == 'brush':
                        if pre_dot != (0, 0, 0):
                            cv2.line(plain, (x, y), pre_dot[:2], color, 3)
                            draw_line(ax, (x, y, z), pre_dot, color=color)
                            f.write("b {} {} {}\n".format(x, y, z))
                        pre_dot = (x, y, z)

                    elif draw_mode == 'ball':
                        if center != (0, 0, 0):
                            # print(center, radius)
                            cv2.circle(plain, center=center[:2], color=(0, 255, 255), radius=radius, thickness=3)
                            draw_ball(ax, center, radius)
                            f.write("s {} {} {} {}\n".format(center[0], center[1], center[2], radius))
                            center = (0, 0, 0)
                            radius = 5

                    elif draw_mode == 'line':
                        if begin_dot != (0, 0, 0):
                            cv2.line(img, (x, y), begin_dot[:2], (205, 0, 255), 3)

                    elif draw_mode == 'cuboid':
                        if begin_dot != (0, 0, 0):
                            cv2.rectangle(img, (x, y), begin_dot[:2], (245, 255, 79), 3)

                    elif draw_mode == 'dot':
                        pre_dot = (x, y, z)

                # Eraser
                if firstOpen and secondOpen and not thirdOpen and not fourthOpen:
                    _, x, y, z = lmList[8]
                    cv2.rectangle(plain, (x-15, y-15), (x+15, y+15), (0, 0, 0), -1)
                    cv2.rectangle(img, (x-15, y-15), (x+15, y+15), (255, 255, 255), -1)
                    cv2.rectangle(img, (x-15, y-15), (x+15, y+15), (0, 0, 0), 1)
                    pre_dot = (0, 0, 0)

                if firstOpen and fourthOpen and not secondOpen and not thirdOpen:
                    if draw_mode == 'brush':
                        color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

                    elif draw_mode == 'ball':
                        center = (x, y, z)
                        cv2.circle(img, center=center[:2], color=(0, 200, 200), radius=radius, thickness=3)
                        if int(time.time()) % 2 == 0:
                            radius += 5

                    elif draw_mode == 'dot':
                        cv2.circle(plain, center=pre_dot[:2], color=(0, 255, 35), radius=2, thickness=-1)
                        draw_dot(ax, pre_dot[0], pre_dot[1], pre_dot[2])
                        f.write("d {} {} {}\n".format(pre_dot[0], pre_dot[1], pre_dot[2]))

                    elif draw_mode == 'line':
                        if begin_dot == (0, 0, 0):
                            if time.time()-line_timestamp > 2:
                                begin_dot = (x, y, z)
                        elif abs(begin_dot[0] - x) + abs(begin_dot[1] - y) > 20:
                            cv2.line(plain, (x, y), begin_dot[:2], (205, 0, 255), 3)
                            draw_line(ax, (x, y, z), begin_dot, (205, 0, 255))
                            f.write("l {} {} {} {} {} {}\n".format(x, y, z, begin_dot[0], begin_dot[1], begin_dot[2]))
                            begin_dot = (0, 0, 0)
                            line_timestamp = time.time()

                    elif draw_mode == 'cuboid':
                        if begin_dot == (0, 0, 0):
                            if time.time()-line_timestamp > 2:
                                begin_dot = (x, y, z)
                        elif abs(begin_dot[0] - x) + abs(begin_dot[1] - y) > 20:
                            cv2.rectangle(plain, (x, y), begin_dot[:2], (245, 255, 79), 3)
                            draw_cuboid(ax, (x, y, z), begin_dot, (245, 255, 79))
                            f.write("c {} {} {} {} {} {}\n".format(x, y, z, begin_dot[0], begin_dot[1], begin_dot[2]))
                            begin_dot = (0, 0, 0)
                            line_timestamp = time.time()
                if not firstOpen:
                    pre_dot = (0, 0, 0)
                    center = (0, 0, 0)
            result = cv2.addWeighted(img, 0.7, plain, 0.3, 0)
            img2gray = cv2.cvtColor(panel, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)
            img1_bg = cv2.bitwise_and(result, result, mask=mask_inv)
            display = cv2.add(img1_bg, panel)
            cv2.imshow("image", display)
            cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
            if MODE3D:
                plt.pause(0.1)
            if cv2.waitKey(2) & 0xFF == 27:
                plt.ioff()
                break


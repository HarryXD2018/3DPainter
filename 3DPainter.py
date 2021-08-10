import time, datetime
import cv2
import HandTrackingModule as htm
import numpy as np
import random
from util3d import runtime_init, draw_line, draw_ball, draw_dot, draw_cuboid
from interaction import switch_mode, opt, img2plain, plain2img, coor3d, plain2abs
from gen3d import gen3d
from math import floor

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
    if draw_mode == 'move':
        cv2.rectangle(panel, (160, 0), (480, 40), (116, 153, 255), -1)
        cv2.putText(panel, "L", (200, 20), cv2.FONT_HERSHEY_PLAIN, 1, (46, 255, 224), 1)
        cv2.putText(panel, "T", (280, 20), cv2.FONT_HERSHEY_PLAIN, 1, (46, 255, 224), 1)
        cv2.putText(panel, "B", (360, 20), cv2.FONT_HERSHEY_PLAIN, 1, (46, 255, 224), 1)
        cv2.putText(panel, "R", (440, 20), cv2.FONT_HERSHEY_PLAIN, 1, (46, 255, 224), 1)
    else:
        cv2.rectangle(panel, (160, 0), (480, 40), (0, 0, 0), -1)


def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    global plain, pre_dot, center, draw_mode, show_zone, save_timestamp
    if event == cv2.EVENT_LBUTTONDOWN:
        if x > 520 and y < 40:
            plain = np.zeros((480, 640, 3), np.uint8)
            plt.cla()
            show_zone = [0, 0]
            f.write("clear\n")
            pre_dot = (0, 0, 0)
            center = (0, 0, 0)
        elif x < 120 and y < 40:
            draw_mode = switch_mode(draw_mode)
        elif x > 520 and y > 440:
            f.close()
            if opt.export3d or opt.view3d:
                gen3d()
            exit()
        elif x < 120 and y > 440:
            save_photo()
            save_timestamp = time.time()
            cv2.rectangle(img, (0, 440), (120, 480), (0, 0, 0), -1)


def move_panel(image, x):
    global move_timestamp
    global show_zone, absolute_coor
    if time.time() - move_timestamp < 0.5:
        return image
    move_timestamp = time.time()
    direction = floor((x - 160) / 80)
    f.write("move\n")
    if direction == 1:              # Top
        absolute_coor[1] -= 50
        if show_zone[1] == 0:
            image = cv2.copyMakeBorder(image, 50, 0, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        else:
            show_zone[1] -= 50

    elif direction == 2:
        absolute_coor[1] += 50
        if show_zone[1] + 480 == image.shape[0]:
            image = cv2.copyMakeBorder(image, 0, 50, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        show_zone[1] += 50

    elif direction == 0:
        absolute_coor[0] -= 50
        if show_zone[0] == 0:
            image = cv2.copyMakeBorder(image, 0, 0, 50, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        else:
            show_zone[0] -= 50

    elif direction == 3:
        absolute_coor[0] += 50
        if show_zone[0] + 640 == image.shape[1]:
            image = cv2.copyMakeBorder(image, 0, 0, 0, 50, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        show_zone[0] += 50
    return image


def save_photo():
    now = datetime.datetime.now()
    cv2.imwrite("./output/Image{}.jpg".format(now.strftime("%Y%m%d%H%M%S")), result)


wCam, hCam = 640, 480
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, wCam)
cap.set(4, hCam)


if __name__ == '__main__':
    # Display function init
    plain = np.zeros((480, 640, 3), np.uint8)           # plots
    panel = np.zeros((480, 640, 3), np.uint8)           # bottoms
    show_zone = [0, 0]                                  # the display area
    absolute_coor = [0, 0]                              # the absolute coordinate of the paint
    ax = runtime_init()

    # painting init
    pre_dot = (0, 0, 0)
    begin_dot = (0, 0, 0)
    center = (0, 0, 0)
    color = (255, 255, 0)
    draw_mode = 'cuboid'
    Signature = "H.Chen"
    switch_timestamp = 0
    text_timestamp = 0
    line_timestamp = 0
    move_timestamp = 0
    save_timestamp = 0
    radius = 5

    # hand detectors
    detector = htm.handDetctor(detectionCon=0.7)

    opt.preview3d = False
    opt.view3d = False
    opt.export3d = False

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
                    _, screen_x, screen_y, z = lmList[8]
                    absolute_x, absolute_y = coor3d((screen_x, screen_y), absolute_coor)
                    plain_x, plain_y = img2plain(screen_x, screen_y, show_zone)
                    # Move
                    if draw_mode == 'move':
                        if 160 < screen_x < 480 and screen_y < 40:
                            plain = move_panel(plain, screen_x)

                    # Switch Mode
                    if screen_x < 120 and screen_y < 40 and time.time()-switch_timestamp > 10:
                        switch_timestamp = time.time()
                        draw_mode = switch_mode(draw_mode)
                        pre_dot = (0, 0, 0)

                    # Clear Plain
                    elif screen_x > 360 and screen_y < 40:
                        plain = np.zeros((480, 640, 3), np.uint8)
                        plt.cla()
                        pre_dot = (0, 0, 0)
                        center = (0, 0, 0)
                        show_zone = [0, 0]
                        f.write("clear\n")
                    else:
                        if draw_mode == 'brush':
                            if pre_dot != (0, 0, 0):
                                cv2.line(plain, (plain_x, plain_y), pre_dot[:2], color, 3)
                                draw_line(ax, (absolute_x, absolute_y, z),
                                          plain2abs(pre_dot, coor=absolute_coor, zone=show_zone), color=color)
                                f.write("b {} {} {} {} {} {}\n".format(absolute_x, absolute_y, z,
                                                                       color[2], color[1], color[0]))
                            pre_dot = (plain_x, plain_y, z)

                        elif draw_mode == 'ball':
                            if center != (0, 0, 0):
                                cv2.circle(plain, center=center[:2], color=(0, 255, 255), radius=radius, thickness=-1)
                                draw_ball(ax, plain2abs(center, coor=absolute_coor, zone=show_zone), radius)
                                str_temp = list(map(str, plain2abs(center, coor=absolute_coor, zone=show_zone)))
                                str_temp = " ".join(str_temp)
                                f.write("s " + str_temp + " {}\n".format(radius))
                                center = (0, 0, 0)
                                radius = 5

                        elif draw_mode == 'line':
                            if begin_dot != (0, 0, 0):
                                cv2.line(img, (screen_x, screen_y),
                                         plain2img(begin_dot[0], begin_dot[1], show_zone), (205, 0, 255), 3)

                        elif draw_mode == 'cuboid':
                            if begin_dot != (0, 0, 0):
                                cv2.rectangle(img, (screen_x, screen_y),
                                              plain2img(begin_dot[0], begin_dot[1], show_zone), (245, 255, 79), 3)

                        elif draw_mode == 'dot':
                            pre_dot = (plain_x, plain_y, z)

                # Eraser
                if firstOpen and secondOpen and not thirdOpen and not fourthOpen:
                    _, screen_x, screen_y, z = lmList[8]
                    plain_x, plain_y = img2plain(screen_x, screen_y, show_zone)
                    cv2.rectangle(plain, (plain_x-15, plain_y-15), (plain_x+15, plain_y+15), (0, 0, 0), -1)
                    cv2.rectangle(img, (screen_x - 15, screen_y - 15), (screen_x + 15, screen_y + 15), (255, 255, 255), -1)
                    cv2.rectangle(img, (screen_x - 15, screen_y - 15), (screen_x + 15, screen_y + 15), (0, 0, 0), 1)
                    pre_dot = (0, 0, 0)

                if firstOpen and fourthOpen and not secondOpen and not thirdOpen:
                    _, screen_x, screen_y, z = lmList[8]
                    absolute_x, absolute_y = coor3d((screen_x, screen_y), absolute_coor)
                    plain_x, plain_y = img2plain(screen_x, screen_y, show_zone)
                    if draw_mode == 'brush':
                        color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

                    # Template, don't draw on img
                    elif draw_mode == 'ball':
                        center = (plain_x, plain_y, z)
                        cv2.circle(img, center=(screen_x, screen_y), color=(0, 200, 200), radius=radius, thickness=3)
                        if int(time.time()) % 2 == 0:
                            radius += 5

                    elif draw_mode == 'dot':
                        cv2.circle(plain, center=(plain_x, plain_y), color=(0, 255, 35), radius=2, thickness=-1)
                        draw_dot(ax, (absolute_x, absolute_y, z))
                        str_temp = list(map(str, plain2abs(pre_dot, absolute_coor, show_zone)))
                        f.write("d " + " ".join(str_temp) + " \n")

                    elif draw_mode == 'line':
                        if begin_dot == (0, 0, 0):
                            if time.time()-line_timestamp > 2:
                                begin_dot = (plain_x, plain_y, z)
                        elif abs(begin_dot[0] - plain_x) + abs(begin_dot[1] - plain_y) > 20:
                            cv2.line(plain, (plain_x, plain_y), begin_dot[:2], (205, 0, 255), 3)
                            draw_line(ax, (absolute_x, absolute_y, z),
                                      plain2abs(begin_dot, absolute_coor, show_zone), (205, 0, 255))
                            str_temp = list(map(str, plain2abs(begin_dot, absolute_coor, show_zone)))
                            f.write("l {} {} {} ".format(absolute_x, absolute_y, z) + " ".join(str_temp) + "\n")
                            begin_dot = (0, 0, 0)
                            line_timestamp = time.time()

                    elif draw_mode == 'cuboid':
                        if begin_dot == (0, 0, 0):
                            if time.time()-line_timestamp > 2:
                                begin_dot = (plain_x, plain_y, z)
                        elif abs(begin_dot[0] - plain_x) + abs(begin_dot[1] - plain_y) > 20:
                            cv2.rectangle(plain, (plain_x, plain_y), begin_dot[:2], (245, 255, 79), -1)
                            draw_cuboid(ax, (absolute_x, absolute_y, z),
                                        plain2abs(begin_dot, absolute_coor, show_zone), (245, 255, 79))
                            str_temp = list(map(str, plain2abs(begin_dot, absolute_coor, show_zone)))
                            f.write("c {} {} {} ".format(plain_x, plain_y, z) + " ".join(str_temp) + " \n")
                            begin_dot = (0, 0, 0)
                            line_timestamp = time.time()

                    elif draw_mode == 'text':
                        if time.time()-text_timestamp > 2:
                            cv2.putText(plain, Signature, (plain_x, plain_y), cv2.FONT_HERSHEY_PLAIN, 3, (102, 248, 255), 1)
                            f.write("t {} {} {} {}\n".format(absolute_x, absolute_y, z, Signature))
                            text_timestamp = time.time()
                if not firstOpen:
                    pre_dot = (0, 0, 0)
                    center = (0, 0, 0)

            temp = plain[show_zone[1]: (show_zone[1]+480), show_zone[0]: (show_zone[0]+640)]
            cv2.imshow("full view", plain)

            if time.time() - save_timestamp < 0.4:          # camera shooter effect
                img = cv2.add(img, img)

            result = cv2.addWeighted(img, 0.7, temp, 0.3, 0)
            img2gray = cv2.cvtColor(panel, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)
            img1_bg = cv2.bitwise_and(result, result, mask=mask_inv)
            display = cv2.add(img1_bg, panel)
            cv2.imshow("image", display)
            cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
            if opt.preview3d:
                plt.pause(0.1)
            if cv2.waitKey(2) & 0xFF == 27:
                plt.ioff()
                break


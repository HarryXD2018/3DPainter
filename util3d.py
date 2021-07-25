import matplotlib.pyplot as plt
import time
from mpl_toolkits.mplot3d import Axes3D
import cv2
import numpy as np


def draw_line(ax, pt1, pt2, color='blue'):
    if MODE3D:
        print("draw line")
        x1, y1, z1 = pt1
        x2, y2, z2 = pt2
        ax.plot([x1, x2], [-y1, -y2], [z1, z2], color)


def draw_ball(ax, center, radius, color='Reds'):
    if MODE3D:
        t = np.linspace(0, np.pi * 2, 100)
        s = np.linspace(0, np.pi, 100)
        t, s = np.meshgrid(t, s)
        x = radius * np.cos(t) * np.sin(s) + center[0]
        y = -radius * np.sin(t) * np.sin(s) - center[1]
        z = radius * np.cos(s) + center[2]
        # ax = plt.subplot(111, projection='3d')
        ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap=color)


def runtime_init():
    # plt.ion()
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('x axis') #x轴名称
    ax.set_ylabel('y axis') #y轴名称
    ax.set_zlabel('z axis')
    ax.view_init(elev=85, azim=-87)
# ax.axis('equal')
    return ax


MODE3D = True


if __name__ == '__main__':
    # plt.ion()
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, projection='3d')
    # draw_line(ax, (10, 10, 10), (20, 20, 20))
    draw_ball(ax, (100, 100, 100), 5)
    # draw_line(ax, (0, 0, 0), (10, 10, 10))
    draw_ball(ax, (10, 5, 5), 5)
    plt.show()
    # plt.ioff()




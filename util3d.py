import matplotlib.pyplot as plt
import numpy as np
from interaction import opt


def bgr2plt(color):
    return color[2]/255, color[1]/255, color[0]/255


def draw_line(ax, pt1, pt2, color):
    if opt.preview3d:
        # print("draw line")
        x1, y1, z1 = pt1
        x2, y2, z2 = pt2
        ax.plot([x1, x2], [-y1, -y2], [z1, z2], color=bgr2plt(color))


def draw_ball(ax, center, radius, color='Reds'):
    if opt.preview3d:
        t = np.linspace(0, np.pi * 2, 100)
        s = np.linspace(0, np.pi, 100)
        t, s = np.meshgrid(t, s)
        x = radius * np.cos(t) * np.sin(s) + center[0]
        y = -radius * np.sin(t) * np.sin(s) - center[1]
        z = radius * np.cos(s) + center[2]
        # ax = plt.subplot(111, projection='3d')
        ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap=color)


def draw_dot(ax, pt):
    if opt.preview3d:
        ax.scatter(pt[0], -pt[1], pt[2], color=(0, 1, 0.14))


def draw_cuboid(ax, pt1, pt2, color=(245, 255, 79)):
    if opt.preview3d:
        xx = np.linspace(pt1[0], pt2[0], 2)
        yy = np.linspace(-pt1[1], -pt2[1], 2)
        zz = np.linspace(pt1[2], pt2[2], 2)
        xx2, yy2 = np.meshgrid(xx, yy)
        ax.plot_surface(xx2, yy2, np.full_like(xx2, pt1[2]), color=bgr2plt(color))
        ax.plot_surface(xx2, yy2, np.full_like(xx2, pt2[2]), color=bgr2plt(color))
        yy2, zz2 = np.meshgrid(yy, zz)
        ax.plot_surface(np.full_like(yy2, pt1[0]), yy2, zz2, color=bgr2plt(color))
        ax.plot_surface(np.full_like(yy2, pt2[0]), yy2, zz2, color=bgr2plt(color))
        xx2, zz2= np.meshgrid(xx, zz)
        ax.plot_surface(xx2, np.full_like(yy2, -pt1[1]), zz2, color=bgr2plt(color))
        ax.plot_surface(xx2, np.full_like(yy2, -pt2[1]), zz2, color=bgr2plt(color))


def runtime_init():
    if opt.preview3d:
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('screen_x axis') #x轴名称
        ax.set_ylabel('screen_y axis') #y轴名称
        ax.set_zlabel('z axis')
        ax.view_init(elev=85, azim=-87)
        return ax


if __name__ == '__main__':
    # plt.ion()
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, projection='3d')
    # draw_line(ax, (10, 10, 10), (20, 20, 20))
    # draw_ball(ax, (100, 100, 100), 5)
    # # draw_line(ax, (0, 0, 0), (10, 10, 10))
    # draw_ball(ax, (10, 5, 5), 5)
    # draw_dot(ax, 1, 2, 3)
    draw_cuboid(ax, (0, 0, 0), (2, 3, 3))
    plt.show()
    # plt.ioff()




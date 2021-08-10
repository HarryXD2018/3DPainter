import cv2
import numpy as np
from open3d import PointCloud, Vector3dVector, draw_geometries
import open3d as o3d
import datetime
import random
from interaction import opt


def pc_cube(pt1, pt2):
    x = np.linspace(pt1[0], pt2[0])
    y = np.linspace(pt1[1], pt2[1])
    z = np.linspace(pt1[2], pt2[2])

    x1, y1 = np.meshgrid(x, y)
    X = x1.ravel()
    Y = y1.ravel()
    face1 = np.c_[X, Y, np.full_like(X, pt1[2])]
    face2 = np.c_[X, Y, np.full_like(X, pt2[2])]

    z1, y1= np.meshgrid(z, y)
    Z = z1.ravel()
    Y = y1.ravel()
    face3 = np.c_[np.full_like(Z, pt1[0]), Y, Z]
    face4 = np.c_[np.full_like(Z, pt2[0]), Y, Z]

    x1, z1 = np.meshgrid(x, z)
    X = x1.ravel()
    Z = z1.ravel()
    face5 = np.c_[X, np.full_like(X, pt1[1]), Z]
    face6 = np.c_[X, np.full_like(X, pt2[1]), Z]

    ans = np.concatenate((face1, face2, face3, face4, face5, face6))
    return ans


def pc_line(pt1, pt2):
    alpha = 5 * int(np.linalg.norm(np.asarray(pt1)-np.asarray(pt2)))
    x = np.linspace(pt1[0], pt2[0], alpha)
    y = np.linspace(pt1[1], pt2[1], alpha)
    z = np.linspace(pt1[2], pt2[2], alpha)
    return np.c_[x, y, z]


def pc_sphere(center, radius):
    t = np.linspace(0, np.pi * 2, 100)
    s = np.linspace(0, np.pi, 100)
    t, s = np.meshgrid(t, s)
    x = radius * np.cos(t) * np.sin(s) + center[0]
    y = radius * np.sin(t) * np.sin(s) + center[1]
    z = radius * np.cos(s) + center[2]
    return np.c_[x.ravel(), y.ravel(), z.ravel()]


def pc_text(pt1, text: str):
    img = np.ones((480, 640, 3), np.uint8)
    cv2.putText(img, text, (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    x, y = np.where(gray == 0)
    x += pt1[1] - 100
    y += pt1[0] - 100
    black = np.c_[y, x]
    points = np.zeros((1, 3))
    for i in range(10):
        selected_index = random.sample(range(len(black)), random.randint(int(len(black)/3), int(2*len(black)/3)))
        for j in selected_index:
            temp = np.append(black[j], i+pt1[2]).reshape(1, 3)
            points = np.concatenate((points, temp))
    return np.delete(points, 0, axis=0)


def gen3d():
    points = np.zeros((1, 3))
    color = np.zeros((1, 3))
    brush_temp = None
    with open('trace.txt') as f:
        for index, line in enumerate(f):
            info = line.strip().split(' ')
            try:
                nums = list(map(int, info[1:]))
            except ValueError:
                nums = list(map(int, info[1:4]))
            if info[0] == "c":          # cuboid
                append_points = pc_cube(nums[:3], nums[3:])
                append_color = np.ones(append_points.shape) * np.asarray([0.30, 1, 0.96])
                points = np.concatenate((points, append_points))
                color = np.concatenate((color, append_color))
                brush_temp = None
            elif info[0] == "d":        # dots
                append_points = np.asarray(nums).reshape(1, 3)
                points = np.concatenate((points, append_points))
                color = np.concatenate((color, np.asarray([0.001, 1, 0]).reshape((1, 3))))
                brush_temp = None
            elif info[0] == "s":        # sphere
                append_points = pc_sphere(nums[:3], nums[-1])
                append_color = np.ones(append_points.shape) * np.asarray([1, 1, 0])
                points = np.concatenate((points, append_points))
                color = np.concatenate((color, append_color))
                brush_temp = None
            elif info[0] == "l":        # line
                append_points = pc_line(nums[:3], nums[3:])
                append_color = np.ones(append_points.shape) * np.asarray([1, 0, 0.8])
                points = np.concatenate((points, append_points))
                color = np.concatenate((color, append_color))
                brush_temp = None
            elif info[0] == "b":                    # brush
                if brush_temp is not None:
                    append_points = pc_line(nums[:3], brush_temp)
                    append_color = np.ones(append_points.shape) * (np.asarray(nums[3:]) / 255)
                    points = np.concatenate((points, append_points))
                    color = np.concatenate((color, append_color))
                brush_temp = nums[:3]           # 3d
            elif info[0] == "t":                    # text
                if len(info) == 5:
                    append_points = pc_text(nums, info[-1])
                    points = np.concatenate((points, append_points))
                else:
                    text = " ".join(info[i] for i in range(4, len(info)))
                    append_points = pc_text(nums, text)
                    points = np.concatenate((points, append_points))
                append_color = np.ones(append_points.shape) * np.asarray([1, 0.97, 0.4])
                color = np.concatenate((color, append_color))
                brush_temp = None
            elif info[0] == 'clear':
                points = np.ones((1, 3))
            elif info[0] == 'move':
                brush_temp = None
    points = np.delete(points, 0, axis=0)
    color = np.delete(color, 0, axis=0)
    point_cloud = PointCloud()
    point_cloud.points = Vector3dVector(points)
    point_cloud.colors = Vector3dVector(color)
    now = datetime.datetime.now()
    if opt.export3d:
        o3d.io.write_point_cloud('output/{}.ply'.format(now.strftime("%Y%m%d%H%M%S")), point_cloud, True)
    if opt.view3d:
        draw_geometries([point_cloud])


if __name__ == '__main__':
    opt.export3d = False
    gen3d()






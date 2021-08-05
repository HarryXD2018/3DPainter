def switch_mode(cur_mode):
    mode = ['brush', 'ball', 'dot', 'line', 'cuboid', 'text', 'move']
    id = mode.index(cur_mode)
    # print(id)
    next_id = (id + 1) % len(mode)
    return mode[next_id]


def img2plain(x, y, zone):
    return x + zone[0], y + zone[1]


def plain2img(x, y, zone):
    return x - zone[0], y - zone[1]


def coor3d(pt, coor):
    if len(pt) == 3:
        return pt[0] + coor[0], pt[1] + coor[1], pt[2]
    else:
        return pt[0] + coor[0], pt[1] + coor[1]


def plain2abs(pt, coor, zone):
    return pt[0] + coor[0] - zone[0], pt[1] + coor[1] - zone[1], pt[2]


class Options:
    def __init__(self):
        self.preview3d = True           # Enable matplotlib 3d synchronized preview
        self.export3d = True
        self.view3d = True          # View the ply result in the final


opt = Options()


if __name__ == '__main__':
    print(switch_mode("ball"))
    print(switch_mode("brush"))

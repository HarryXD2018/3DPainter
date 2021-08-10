import datetime
import os

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


def project_init():
    now = datetime.datetime.now()
    project_name = "Project_" + now.strftime("%m_%d_%H_%M")
    os.mkdir('./output/'+project_name)
    return project_name



def plain2abs(pt, coor, zone):
    return pt[0] + coor[0] - zone[0], pt[1] + coor[1] - zone[1], pt[2]


class Options:
    def __init__(self, preview3d: bool = True,
                 export3d: bool = True,
                 view3d: bool = True,
                 view3d_trace: bool = True,
                 pc_color: str = 'default'):
        self.preview3d = preview3d          # Enable matplotlib 3d synchronized preview
        self.export3d = export3d
        self.view3d_trace = view3d_trace
        self.pc_color = pc_color            # rainbow or default
        self.view3d = view3d                # View the ply result in the final


opt = Options()


if __name__ == '__main__':
    project_init()

def switch_mode(cur_mode):
    mode = ['brush', 'ball', 'dot', 'line', 'cuboid', 'text']
    id = mode.index(cur_mode)
    # print(id)
    next_id = (id + 1) % len(mode)
    return mode[next_id]


class Options:
    def __init__(self):
        self.preview3d = True           # Enable matplotlib 3d synchronized preview
        self.export3d = True
        self.view3d = True          # View the ply result in the final


opt = Options()


if __name__ == '__main__':
    print(switch_mode("ball"))
    print(switch_mode("brush"))

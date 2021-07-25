def switch_mode(cur_mode):
    mode = ['ball', 'pencil']
    id = mode.index(cur_mode)
    # print(id)
    next_id = (id + 1) % len(mode)
    return mode[next_id]


if __name__ == '__main__':
    print(switch_mode("ball"))
    print(switch_mode("pencil"))

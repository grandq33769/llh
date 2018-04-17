from enum import Enum
from itertools import product
import numpy as np

ACTION = Enum('ACTION', 'Up Down Left Right')
ACT_DICT = {
    ACTION.Up: (lambda coor: (coor[0], coor[1] + 1)),
    ACTION.Down: (lambda coor: (coor[0], coor[1] - 1)),
    ACTION.Left: (lambda coor: (coor[0] - 1, coor[1])),
    ACTION.Right: (lambda coor: (coor[0] + 1, coor[1]))
}
W, H = 4, 4
END = {(0, 0), (3, 3)}
REWARD = -1


def policy_iteration():
    # Initialization
    k = 0
    value_table = np.zeros((W, H))
    pre_vtable = None
    policy_table = dict()
    for x, y in product(range(W), range(H)):
        if (x, y) in END: continue
        policy_table.update({
            (x, y): {ACTION.Up, ACTION.Down, ACTION.Left, ACTION.Right}
        })
    print('k = {}'.format(k))
    print(value_table)

    # Policy Evaluation
    while not np.array_equal(value_table, pre_vtable):
        k += 1
        print('k = {:d}'.format(k))
        pre_vtable = np.array(value_table)
        for x, y in product(range(W), range(H)):
            if (x, y) in END: continue
            v = value_eval((x, y), pre_vtable, policy_table)
            value_table[x][y] = v
        print(value_table)


def value_eval(coor, vtable, ptable):
    v_list = map(lambda x: action_eval(x, coor, vtable), ptable[coor])
    value = sum(v_list)

    return value / len(ptable[coor])


def action_eval(action, coor, vtable):
    target = ACT_DICT[action](coor)
    if not coor_verify(target):
        target = coor
    return REWARD + vtable[target[0]][target[1]]


def coor_verify(coor):
    if coor[0] < 0 or coor[0] > W - 1:
        return False
    elif coor[1] < 0 or coor[1] > H - 1:
        return False
    else:
        return True


if __name__ == '__main__':
    policy_iteration()

'''Mining Sequential Frequent Pattern'''
import functools as ft
from itertools import product
from arrange import ARRANGE_LIST

RESULT_DICT = {}


def update_dict(dic, com, result):
    '''Sum up the combination result'''
    tuple_of_combination = [tuple(x) for x in com]
    for key in tuple_of_combination:
        if key in dic:
            value = dic[key]
            # Number of times of sequence happened
            value[0] += 1
            # Average of number of disease (Incremental Average)
            value[1] += (result[com.index(key)] - value[1]) / value[0]
            dic.update({key: value})
        else:
            value = [1, result[com.index(key)]]
            dic.update({key: value})


def list_of_number(alist, raw):
    '''return number of disease from a list of location'''
    return [raw[x][alist[x]] for x in range(0, len(raw))]


def sequential_mining(result_dict, arrange_list, length, window_size):
    '''Mining Algorithm'''

    diff = len(arrange_list) - length
    if diff + window_size <= len(arrange_list):
        print('Time {} begin...'.format(diff))
        raw = [arrange_list[x] for x in range(diff, diff + window_size)]
        corpus = [x.keys() for x in raw]
        combination = [x for x in product(*corpus)]
        number = map(ft.partial(list_of_number, raw=raw), combination)
        result = [sum(x) for x in number]
        update_dict(result_dict, combination, result)
        sequential_mining(result_dict, arrange_list, length - 1, window_size)

    else:
        return


sequential_mining(RESULT_DICT, ARRANGE_LIST, len(ARRANGE_LIST), 4)

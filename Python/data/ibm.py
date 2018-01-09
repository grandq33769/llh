'''
To import IBM synthetic data as python data structure from .data
Date : 2017/10/23
'''


def process_line(line):
    '''
    Args:
        line(str): String line read from .data 
    Returns:
        index(str): Index represent the tuple
        value(str): Value of tuple
    '''
    lis = list(filter(None, line[:-1].split(' ')))
    return lis[0], lis[2]


def open_data(tlen, item, num):
    '''
    Input & Rescalling Anime data
    Place .data path in root directory
    Args:
        tlen(int): Transaction lenght
        item(int): Potential maximum pattern
        num(int): Number of transaction
    '''
    r_list = list()
    name = 'T{}I{}D{}.data'.format(str(tlen), str(item), str(num))
    with open(name, 'r') as file:
        t_list = []
        first = file.readline()
        idx, value = process_line(first)
        t_list.append(value)
        for line in file.readlines():
            n_idx, value = process_line(line)
            if idx != n_idx:
                r_list.append(tuple(t_list))
                t_list = []

            t_list.append(value)
            idx = n_idx

        return tuple(r_list)

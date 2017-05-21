'''Demo script for sharing memory in multiprocessing'''
from multiprocessing import Process, Value, Array
import os


def info(title):
    '''A function for print out the information'''
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def func(number, array, value):
    '''Testing function'''
    info('function f')
    number.value = 3.1415927
    for member in enumerate(array):
        array[member[0]] = value
    print('Array in process: ', array)


if __name__ == '__main__':
    info('main')
    NUM = Value('d', 0.0)
    ARR = Array('i', range(10))
    ARR2 = list(range(10))

    P1 = Process(target=func, args=(NUM, ARR, 2))
    P2 = Process(target=func, args=(NUM, ARR, 3))
    P1.start()
    P2.start()
    P1.join()
    P2.join()

    print('\n', NUM.value)
    print('Array: ', ARR[:], '\n')

    P1 = Process(target=func, args=(NUM, ARR2, 2))
    P2 = Process(target=func, args=(NUM, ARR2, 3))
    P1.start()
    P2.start()
    P1.join()
    P2.join()

    print('Array2: ', ARR2[:])

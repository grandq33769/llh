'''Simple example for multiprocessing'''
from multiprocessing import Process
import os


def info(title):
    '''Show information of process'''
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def func(name):
    '''Testing function'''
    info('function f')
    print('hello', name)


if __name__ == '__main__':
    info('main line')
    PROC = Process(target=func, args=('bob',))
    PROC.start()
    PROC.join()

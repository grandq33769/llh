'''Demo script for synchronization of multiprocessing'''
from multiprocessing import Process, Lock


def func(lock, num):
    '''Testing function for using lock'''
    lock.acquire()
    try:
        for _ in range(1000):
            print('hello world', num)
    finally:
        lock.release()


if __name__ == '__main__':
    LOCK = Lock()

    for n in range(10):
        Process(target=func, args=(LOCK, n)).start()

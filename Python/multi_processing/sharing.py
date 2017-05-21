from multiprocessing import Process, Value, Array
import os


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def f(n, a, v):
    info('function f')
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = v
    print('arr in process: ', a)


if __name__ == '__main__':
    info('main')
    num = Value('d', 0.0)
    arr = Array('i', range(10))
    arr2 = list(range(10))

    p1 = Process(target=f, args=(num, arr, 2))
    p2 = Process(target=f, args=(num, arr, 3))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print('\n', num.value)
    print('arr: ', arr[:], '\n')

    p1 = Process(target=f, args=(num, arr2, 2))
    p2 = Process(target=f, args=(num, arr2, 3))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print('arr2: ', arr2[:])

from multiprocessing import Process, Lock


def f(l, i):
    l.acquire()
    try:
        for _ in range(1000):
            print('hello world', i)
    finally:
        pass
        l.release()


if __name__ == '__main__':
    lock = Lock()

    for num in range(10):
        Process(target=f, args=(lock, num)).start()

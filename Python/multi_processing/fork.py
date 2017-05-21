'''Simple example for forking'''
import multiprocessing as mp
TLIST = list(range(10))


def func(pipe):
    '''Testing Function'''
    pipe.send(TLIST)
    pipe.close()


if __name__ == '__main__':
    CTX = mp.get_context('fork')  # 'spawn' for window
    PI_1, PI_2 = CTX.Pipe()
    P1 = CTX.Process(target=func, args=(PI_1,))
    P1.start()
    print(PI_2.recv())
    P1.join()

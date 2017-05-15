'''Simple example for forking'''
import multiprocessing as mp
tlist = list(range(10))


def foo(pipe):
    '''Testing Function'''
    pipe.send(tlist)
    pipe.close()


if __name__ == '__main__':
    CTX = mp.get_context('fork')
    pi_1, pi_2 = CTX.Pipe()
    p1 = CTX.Process(target=foo, args=(pi_1,))
    p1.start()
    print(pi_2.recv())
    p1.join()

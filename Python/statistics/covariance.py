'''
Example program to learn covarience
Date: 2017/09/11
'''
import numpy as np

A = [5.4, -4.2, 10.4, 11.2, -7.8, -2]
B = [3.4, -1.2, 7.5, 5.2, 3, -5]


def covarience(xlist, ylist):
    '''
    Function for calculate covarience between two lists
    Input: list(float), list(float)
    Output: float
    '''
    if len(xlist) != len(ylist):
        raise ArithmeticError('Different lenght of two list.')
    else:
        lenght = len(A)
        xavg = np.average(xlist)
        yavg = np.average(ylist)
        total = 0.0
        for index in range(lenght):
            total += (xlist[index] - xavg) * (ylist[index] - yavg)
        return 1 / (lenght - 1) * total


def correlation(xlist, ylist):
    '''
    Function for calculate Correlation codfficient between two lists
    Input: list(float), list(float)
    Output: float
    '''
    if len(xlist) != len(ylist):
        raise ArithmeticError('Different lenght of two list.')
    else:
        return covarience(xlist, ylist) / np.sqrt(covarience(xlist, xlist) * covarience(ylist, ylist))


if __name__ == '__main__':
    print('lenght: A:{:d} B:{:d}'.format(len(A), len(B)))
    print('A: ', A)
    print('B: ', B)
    print('Average: A:{:.3f} B:{:.3f}'.format(np.average(A), np.average(B)))

    print('Covarience: {:.3f}'.format(covarience(A, B)))
    # Note: numpy std divide N & numpy cov divide N-1
    print('Std: A:{:.3f} B:{:.3f}'.format(np.std(A), np.std(B)))
    print('Correlation coefficient: {:.3f}'.format(correlation(A, B)))

    # Using numpy module
    STACK = np.vstack((A, B))
    print(STACK)
    print(np.cov(STACK))
    print(np.corrcoef(STACK))

'''Module for ploting graph'''
from llh.Python.regression.housing \
    import ATTR_NAME, INPUT_INDEX, TARGET_INDEX
from llh.Python.regression.housing.data_input import TARGET_LIST

import matplotlib.pyplot as plt
import numpy as np
import pylab as mpl

# Chinese Chracter
mpl.rcParams['font.sans-serif'] = ['heit']
mpl.rcParams['axes.unicode_minus']

# my result : weight:-0.95 bias: 34.54
# my result 2 : weight:-2.3272 weight2:0.0434 bias:42.8169

X = np.arange(0, 40)
Y = -0.95 * X + 34.54
Y2 = -2.3272 * X + 0.0434 * X**2 + 42.8169

plt.xlabel(ATTR_NAME[INPUT_INDEX])
plt.ylabel(ATTR_NAME[TARGET_INDEX])
for member in TARGET_LIST:
    plt.scatter(member[0], member[1], color='blue')
plt.plot(X, Y, 'r')
plt.plot(X, Y2, color='#D9B611')
plt.title(u'中文')

plt.show()

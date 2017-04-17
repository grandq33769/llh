'''
Created on 2017�?4???6?��

@author: LokHim
'''

import matplotlib.pyplot as plt
import numpy as np


x = np.arange(0, 360)
y = np.sin(x * np.pi / 180.0)

plt.plot(x, y)
plt.xlim(-30, 390)
plt.ylim(-1.5, 1.5)
plt.xlabel("x-axis")
plt.ylabel("y-axis")
plt.title("The Title")

plt.show()

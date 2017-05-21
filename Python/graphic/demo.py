'''Demo script for using matplotlib to plot graph'''
import matplotlib.pyplot as plt
import numpy as np


X = np.arange(0, 360)
Y = np.sin(X * np.pi / 180.0)

plt.plot(X, Y)
plt.xlim(-30, 390)
plt.ylim(-1.5, 1.5)
plt.xlabel("x-axis")
plt.ylabel("y-axis")
plt.title("The Title")

plt.show()

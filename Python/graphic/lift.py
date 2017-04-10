'''
Created on 2017年4月10日

@author: LokHim
'''
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

fig = plt.figure()
ax = fig.gca(projection='3d')

x = np.arange(0.1, 1,0.1)
y = np.arange(0.1, 1,0.1)
x, y = np.meshgrid(x, y)
z = x / y

surf = ax.plot_surface(x, y, z, cmap=cm.YlGnBu, linewidth=0, antialiased=False)
ax.set_xlabel('x:Confidence')
ax.set_ylabel('y:Probability of b')
ax.set_zlabel('z:Lift')
ax.set_zlim(0,10)

plt.title('z = x/y')
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()

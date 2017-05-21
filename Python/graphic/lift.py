'''Demo script for plotting lift graph of association rule'''
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import AXes3d  # @UnresolvedImport
import numpy as np


FIG = plt.figure()
AX = FIG.gca(projection='3d')

CONFIDENCE = np.arange(0.1, 1, 0.1)
PROB_LEFT = np.arange(0.1, 1, 0.1)
CONFIDENCE, PROB_LEFT = np.meshgrid(CONFIDENCE, PROB_LEFT)
LIFT = CONFIDENCE / PROB_LEFT

SURF = AX.plot_surface(CONFIDENCE, PROB_LEFT,
                       LIFT, cmap=cm.YlGnBu, linewidth=0, antialiased=False)
AX.set_xlabel('Confidence')
AX.set_ylabel('Probability of left')
AX.set_zlabel('Lift')
AX.set_zlim(0, 10)

plt.title('Change of Lift')
FIG.colorbar(SURF, shrink=0.5, aspect=5)

plt.show()

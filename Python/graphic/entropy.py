'''
Script for plotting entropy
Date: 2017/11/30
'''
import matplotlib.pyplot as plt
import numpy as np

FIG = plt.figure()

PROB = np.linspace(0, 1, 100)
OUTPUT = -PROB * np.log2(PROB) - (1 - PROB) * np.log(1 - PROB)
print(OUTPUT)

plt.plot(PROB, OUTPUT)
plt.xlabel("Probability")
plt.ylabel("Entropy")
plt.title("Function of Entropy")

plt.show()

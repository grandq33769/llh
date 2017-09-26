'''
Module for praticing matrix multiply
Date:2017/9/22
'''
import numpy as np

A = np.matrix([1, 2, 3])
ICM = np.matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
AT = np.transpose(A)

print(A * ICM * AT)
print(np.trace(A * ICM * AT))
print(np.trace(AT * A * ICM))
print(np.trace(ICM * AT * A))
RESULT = np.multiply(A * AT, ICM)
print(np.trace(RESULT))

print(A * AT)
print(AT * A)
print(np.linalg.det(ICM))

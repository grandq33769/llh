'''
Created on 2017年5月3日

@author: LokHim
'''
from PIL import Image
from input import *
import numpy as np
import math as m

def trigonoTransform(angle,function):
    return function((angle*m.pi)/180)

def angleRotate(x,y,angle):
    cos_v = trigonoTransform(angle, m.cos)
    sin_v = trigonoTransform(angle, m.sin)
    return (cos_v*x - sin_v*y) , (sin_v*x + cos_v*y)

def transformRGB(r,g,b,imagearr):
    r_row, g_row, b_row = []
    for row in imagearr:
        for pixel in row:
            pass
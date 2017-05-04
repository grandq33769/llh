'''
Created on 2017年5月3日

@author: LokHim
'''
from PIL import Image
from input import *
import numpy as np

def transformRGB(r,g,b,imagearr):
    r_row, g_row, b_row = []
    for row in imagearr:
        for pixel in row:
            
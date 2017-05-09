'''
Created on 2017年5月3日

@author: LokHim
'''
import os
import numpy as np

__all__= ['urlbase','fileset','locationdict']

urlbase = 'D:/U/105-2/Pattern Regonition/Final Project/Data/'
fileset = set()
locationdict = dict()

from input import input_name
from input import input_ellipse
from input import input_image
'''
Created on 2017年5月3日

@author: LokHim
'''
import unittest
import numpy as np
from PIL import Image
from input import *


class Test(unittest.TestCase):

    def testImage(self):
        with Image.open(urlbase + '/2002/08/11/big/img_743.jpg', 'r') as image:
            rgb_image = image.convert('RGB')
            #column first
            r, g, b = rgb_image.getpixel((0, 319))
            arrtest = np.array([r, g, b])
    
            arr = np.array(image)
            #row first
            pixel = arr[319, 0]
            print(arrtest, pixel, len(arr[0]))
    
            self.assertTrue((arrtest == pixel).all(), "Not Equal Pixel")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testImage']
    unittest.main()

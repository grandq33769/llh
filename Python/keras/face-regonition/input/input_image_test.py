'''
Created on 2017年5月17日

@author: LokHim
'''
import unittest
import numpy as np
from PIL import Image
from input_name import URLBASE

class Test(unittest.TestCase):
    

    def test_input_image(self):
        test_arr = np.empty(shape = (5000,12,12,3))
        PATH = URLBASE + '/Training/Positive/'
        with Image.open(PATH + '/2002_07_19_big_img_90_4717281.jpg', 'r') as image:
            arr = np.array(image)
            r_arr = np.reshape(arr, (12,12,3))
            print(r_arr.shape)
            test_arr[0] = r_arr
            print(test_arr.shape)
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_input_image']
    unittest.main()
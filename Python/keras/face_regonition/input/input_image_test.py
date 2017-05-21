'''
Created on 2017年5月17日

@author: LokHim
'''
import unittest
import numpy as np
from PIL import Image
from llh.Python.keras.face_regonition.input.input_name import URLBASE


class Test(unittest.TestCase):
    '''Test for inputting input_image module'''

    @classmethod
    def test_input_image(cls):
        '''Test case for input a image and reshape into specific shape'''
        test_arr = np.empty(shape=(5000, 12, 12, 3))
        path = URLBASE + '/Training/Positive/'
        with Image.open(path + '/2002_07_19_big_img_90_4717281.jpg', 'r') as image:
            arr = np.array(image)
            r_arr = np.reshape(arr, (12, 12, 3))
            print(r_arr.shape)
            test_arr[0] = r_arr
            print(test_arr.shape)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_input_image']
    unittest.main()

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
    def setUp(self):
        self.path = URLBASE + '/Training/12-net/Positive/'
        self.image = Image.open(self.path + '/2002_07_19_big_img_18_3422.jpg','r')

    def tearDown(self):
        self.image.close()

    def test_input_image(self):
        '''Test case for input a image and reshape into specific shape'''
        test_arr = np.empty(shape=(5000, 12, 12, 3))
        arr = np.array(self.image.resize((12,12),Image.BILINEAR))
        r_arr = np.reshape(arr, (12, 12, 3))
        print(r_arr.shape)
        test_arr[0] = r_arr
        print(test_arr.shape)
            
    def test_resize_image(self):
        r_image = self.image.resize((12,12),Image.ANTIALIAS)
        r_image.show()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_input_image']
    unittest.main()

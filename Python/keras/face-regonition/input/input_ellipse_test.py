'''
Created on 2017年5月4日

@author: LokHim
'''
import unittest
from input_name import FILESET
from input_ellipse import LOCATION_DICT


class Test(unittest.TestCase):
    '''Test for input ellipse data'''

    def test_exist(self):
        '''Test case for testing existence of labeled face in data'''
        for name in FILESET:
            if name not in LOCATION_DICT:
                print(name)
            else:
                self.assertTrue(name in LOCATION_DICT, 'Existence of element')

    def test_location(self):
        '''Test case for verifying the data correctness'''
        
        ldict = LOCATION_DICT['2002/08/11/big/img_591']
        self.assertEqual(ldict[0].major_axis, 123.583300, 'Equal content')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testLocation']
    unittest.main()

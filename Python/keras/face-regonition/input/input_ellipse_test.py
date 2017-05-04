'''
Created on 2017年5月4日

@author: LokHim
'''
import unittest
from input import *


class Test(unittest.TestCase):


    def testLocation(self):
        list = locationdict['2002/08/11/big/img_591']
        self.assertEqual(list[0].majorAxis, 123.583300, 'Equal content')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testLocation']
    unittest.main()
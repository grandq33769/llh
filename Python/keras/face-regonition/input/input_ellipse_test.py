'''
Created on 2017年5月4日

@author: LokHim
'''
import unittest
from input import *


class Test(unittest.TestCase):


    def testLocation(self):
        print(locationlist)
        self.assertEqual(locationlist['2002/08/11/big/img_59'], ['123.583300 85.549500 1.265839 269.693400 161.781200'], 'Equal content')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testLocation']
    unittest.main()
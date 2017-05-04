'''
Created on 2017年5月3日

@author: LokHim
'''
import unittest
from input import *

class Test(unittest.TestCase):

    def testName(self):
        self.assertEqual(filelist[0][0], '2002/08/11/big/img_591')
        self.assertEqual(filelist[9][0], '2002/08/31/big/img_18008')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

'''
Created on 2017年5月3日

@author: LokHim
'''
import unittest
import os.path
from input import *

class Test(unittest.TestCase):

    def testFileExist(self):
        for name in fileset :
            path = urlbase+name+'.jpg'
            print(path)
            self.assertTrue(os.path.exists(path), 'file not exist')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

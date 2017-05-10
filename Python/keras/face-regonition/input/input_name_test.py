'''
Created on 2017年5月3日

@author: LokHim
'''
import unittest
import os.path
from input_name import URLBASE, FILESET


class Test(unittest.TestCase):
    '''Test fo file name data'''

    def test_file_exist(self):
        '''Test case for existence of image'''
        for name in FILESET:
            path = URLBASE + name + '.jpg'
            print(path)
            self.assertTrue(os.path.exists(path), 'file not exist')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

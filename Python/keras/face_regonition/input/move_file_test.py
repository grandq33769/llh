'''
Created on 2017年5月17日

@author: LokHim
'''
import os, random
import unittest
import shutil
from input_name import URLBASE

class Test(unittest.TestCase):
    '''Test for moving file '''

    def test_move_file(self):
        '''Test case for moving image to another diretory'''
        SRC = URLBASE + '/Input_Data/Negative/'
        DST = URLBASE + 'Input_Data/Negative/Testing/'
        file = random.choice(os.listdir(SRC))
        file_str = (str(file))
        shutil.move(SRC + file_str, DST+ file_str)

    def test_num_of_file(self):
        SRC = URLBASE + '/Input_Data/Negative/'
        lenght = len([name for name in os.listdir(SRC) if os.path.isfile(SRC + name)])
        print(lenght)
        self.assertTrue(lenght > 0, 'Invaild Lenght')
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
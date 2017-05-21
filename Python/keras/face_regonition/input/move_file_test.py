'''
Created on 2017年5月17日

@author: LokHim
'''
import os
import random
import unittest
import shutil
from llh.Python.keras.face_regonition.input.input_name import URLBASE


class Test(unittest.TestCase):
    '''Test for moving file '''

    def setUp(self):
        self.src = URLBASE + '/Input_Data/Negative/'
        self.dst = URLBASE + 'Input_Data/Negative/Testing/'

    def test_move_file(self):
        '''Test case for moving image to another diretory'''
        file = random.choice(os.listdir(self.src))
        shutil.move(self.src + str(file), self.dst + str(file))

    def test_num_of_file(self):
        '''Test case for counting the number of files'''
        lenght = len([name for name in os.listdir(
            self.src) if os.path.isfile(self.src + name)])
        print(lenght)
        self.assertTrue(lenght > 0, 'Invaild Lenght')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

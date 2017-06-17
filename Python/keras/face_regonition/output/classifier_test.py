'''
Created on 2017年6月15日

@author: LokHim
'''
import unittest
from PIL import Image
from llh.Python.keras.face_regonition.input import URLBASE
from llh.Python.keras.face_regonition.input.crop_image import crop 
from llh.Python.keras.face_regonition.output.classifier import predict 

class Test(unittest.TestCase):

    def setUp(self):
        self.filename = '2003/06/25/big/img_460.jpg'
        self.image = Image.open(URLBASE + '/' + self.filename, 'r')

    def tearDown(self):
        self.image.close()
        
    def testPredict(self):
        croped_list = crop(self.image, (80,80), 4)
        result_list = predict('12-net-calibration',croped_list,self.image)
        self.assertTrue(len(result_list)>0, 'List is  null')
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

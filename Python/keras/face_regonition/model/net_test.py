'''
Created on 2017年5月18日

@author: LokHim
'''
import unittest
import multiprocessing as mp
import numpy as np
from keras.models import load_model
from PIL import Image, ImageDraw
from llh.Python.keras.face_regonition.input import URLBASE
from llh.Python.keras.face_regonition.input.crop_image import crop
from llh.Python.keras.face_regonition.input.input_image import transform
from llh.Python.keras.face_regonition.output.classifier import predict

class Test(unittest.TestCase):
    '''Test for CNN'''

    def setUp(self):
        self.filename = '2002/10/30/big/img_512.jpg'
        self.image = Image.open(URLBASE + '/' + self.filename, 'r')

    def tearDown(self):
        self.image.close()

    def test_net(self):
        '''Test case for one image face detection'''
        draw = ImageDraw.Draw(self.image)
        output = []
        plist = []
        for scale in range (2,10):
            size = scale * 25
            crop_list = (crop(self.image, (int(size*0.7) , size), 8))
            output.extend(predict('12-net-calibration',crop_list,self.image))
                            
        for box in output:
            draw.rectangle(box, outline='red')

        self.image.show()
        self.image.save(URLBASE + '/Example/' +
                        self.filename.replace('/', '_'))

if __name__ == '__main__':
    unittest.main()

'''
Created on 2017年5月18日

@author: LokHim
'''
import unittest
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
        self.filename = '2003/08/12/big/img_894.jpg'
        self.image = Image.open(URLBASE + '/' + self.filename, 'r')

    def tearDown(self):
        self.image.close()

    def test_net(self):
        '''Test case for one image face detection'''
        #Size should be tuned
        crop_list = crop(self.image, (100,100), 4)
        output = predict('12-net',crop_list,self.image)
        draw = ImageDraw.Draw(self.image)
        for box in output:
                draw.rectangle(box, outline='red')

        self.image.show()
        self.image.save(URLBASE + '/Example/' +
                        self.filename.replace('/', '_'))

if __name__ == '__main__':
    unittest.main()

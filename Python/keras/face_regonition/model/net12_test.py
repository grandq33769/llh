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


class Test(unittest.TestCase):
    '''Test for 12-net CNN'''

    def setUp(self):
        self.filename = '2003/08/12/big/img_63.jpg'
        self.image = Image.open(URLBASE + '/' + self.filename, 'r')

    def tearDown(self):
        self.image.close()

    def test_12net(self):
        '''Test case for one image face detection'''
        model = load_model('12-net.h5')
        crop_list = crop(self.image, 12, 4)
        x_train = np.empty(shape=(len(crop_list), 12, 12, 3))
        for index, crop_bbox in enumerate(crop_list):
            crop_image = self.image.crop(crop_bbox)
            x_train[index] = transform(crop_image, (12, 12, 3))

        output = model.predict(x_train)
        draw = ImageDraw.Draw(self.image)
        for index, result in enumerate(output):
            if result[0] < result[1]:
                draw.rectangle(
                    crop_list[index], outline='red')

        self.image.show()
        self.image.save(URLBASE + '/Example/' +
                        self.filename.replace('/', '_'))

    unittest.main()

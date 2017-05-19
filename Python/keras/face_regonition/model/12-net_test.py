'''
Created on 2017年5月18日

@author: LokHim
'''
from Python.keras.face_regonition.model import INPUT_PATH
import numpy as np
import unittest
import sys
sys.path.insert(0, INPUT_PATH)
from keras.models import Model, load_model
from PIL import Image, ImageDraw
from Python.keras.face_regonition.input.input_name import URLBASE
from input.crop_image import crop
from input.input_image import transform


class Test(unittest.TestCase):

    def test_12net(self):
        model = load_model('12-net.h5')
        filename = '2003/08/12/big/img_63.jpg'
        with Image.open(URLBASE + filename, 'r') as image:
            crop_list = crop(image, 12, 4)
            x_train = np.empty(shape=(len(crop_list), 12, 12, 3))
            index = 0
            for crop_bbox in crop_list:
                crop_image = image.crop(crop_bbox)
                arr = transform(crop_image, (12, 12, 3))
                x_train[index] = arr
                index += 1

            output = model.predict(x_train)
            draw = ImageDraw.Draw(image)
            index = 0
            for result in output:
                if result[0] < result[1]:
                    draw.rectangle(
                        crop_list[index], outline='red')

                index += 1

            image.show()
            image.save(URLBASE + '/Example/' + filename.replace('/', '_'))

    unittest.main()

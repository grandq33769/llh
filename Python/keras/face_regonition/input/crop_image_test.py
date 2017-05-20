'''
Created on 2017年5月3日

@author: LokHim
'''
import unittest
import math
import numpy as np
from PIL import Image, ImageDraw
from input_name import URLBASE
from input_ellipse import LOCATION_DICT
from crop_image import crop_face, transform_bbox


class Test(unittest.TestCase):
    '''Test for image input and crop the face image'''

    def setUp(self):
        self.filename = '2002/09/01/big/img_16680.jpg'
        self.image = Image.open(URLBASE + '/' + self.filename, 'r')

    def tearDown(self):
        self.image.close()

    @unittest.skip
    def test_image(self):
        '''Test case for different method to read a pixel'''
        rgb_image = self.image.convert('RGB')
        # row first
        r_p, g_p, b_p = rgb_image.getpixel((0, 319))
        arrtest = np.array([r_p, g_p, b_p])

        arr = np.array(self.image)
        # column first
        pixel = arr[319, 0]
        print(arrtest, pixel, len(arr[0]))

        self.assertTrue((arrtest == pixel).all(), "Not Equal Pixel")

    @unittest.skip
    def test_draw2(self):
        '''Test case 2 for drawing a ellipse on face image'''
        ed_list = LOCATION_DICT[self.filename]
        for ell_data in ed_list:
            x_0, y_0 = ell_data.xcoor - ell_data.minor_axis, \
                ell_data.ycoor - ell_data.major_axis
            x_1, y_1 = ell_data.xcoor + ell_data.minor_axis, \
                ell_data.ycoor + ell_data.major_axis
            overlay = Image.new(
                'RGBA', (math.ceil(x_1 - x_0), 1, math.ceil(y_1 - y_0), 1))
            draw = ImageDraw.Draw(overlay)
            draw.rectangle(
                (0, 0, int(x_1 - x_0), int(y_1 - y_0)), outline='red')

            rotated = overlay.rotate(ell_data.angle, expand=True)
            self.image.paste(rotated, (int(x_0), int(y_0)), rotated)

        self.image.show()

    # Final Method
    def test_draw3(self):
        '''Test case 3 for drawing a ellipse on face image'''
        ed_list = LOCATION_DICT[self.filename]
        for index, ell_data in enumerate(ed_list):
            bbox = transform_bbox(ell_data)
            crop_image = self.image.rotate(ell_data.angle).crop(bbox)
            crop_image.save(URLBASE, '/Example/crop_face_', index, '.jpg')
            crop_image.show()

        save_path = URLBASE + '/Example/Crop/'
        for findex, croped_face in enumerate(crop_face(ed_list, self.image, 12, 4)):
            for iindex, croped_image in enumerate(croped_face):
                croped_image.save(save_path, findex, '_', iindex, '.jpg')
        self.image.show()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testImage']
    unittest.main()

'''
Created on 2017/05/03

@author: LokHim
'''
import unittest
import numpy as np
from PIL import Image, ImageDraw
from input_name import URLBASE
from input_ellipse import LOCATION_DICT


class Test(unittest.TestCase):
    '''Test for image input and crop the face image'''

    @unittest.skip
    def test_image(self):
        '''Test case for different method to read a pixel'''
        with Image.open(URLBASE + '/2002/08/11/big/img_743.jpg', 'r') as image:
            rgb_image = image.convert('RGB')
            # row first
            r_p, g_p, b_p = rgb_image.getpixel((0, 319))
            arrtest = np.array([r_p, g_p, b_p])

            arr = np.array(image)
            # column first
            pixel = arr[319, 0]
            print(arrtest, pixel, len(arr[0]))

            self.assertTrue((arrtest == pixel).all(), "Not Equal Pixel")

    @unittest.skip
    def test_draw(self):
        '''Test case for drawing a ellipse on face image'''
        with Image.open(URLBASE + '/2002/08/26/big/img_265.jpg', 'r') as image:
            ed_list = LOCATION_DICT['2002/08/26/big/img_265']
            for ell_data in ed_list:
                x_0, y_0 = ell_data.x - ell_data.minor_axis, ell_data.y - ell_data.major_axis
                x_1, y_1 = ell_data.x + ell_data.minor_axis, ell_data.y + ell_data.major_axis
                bbox = (x_0, y_0, x_1, y_1)
                print(ell_data.angle, bbox)
                draw = ImageDraw.Draw(image)
                draw.ellipse(bbox, outline='red')

            image.show()

    def test_draw2(self):
        '''Test case 2 for drawing a ellipse on face image'''
        overlay = Image.new('RGBA', (200, 100))
        draw = ImageDraw.Draw(overlay)
        draw.ellipse((0, 0, 200, 100), '#0f0')

        temp_image = Image.new('RGB', (500, 500), '#f00')
        rotated = overlay.rotate(45, expand=True)
        temp_image.paste(rotated, (0, 0), rotated)
        temp_image.show()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testImage']
    unittest.main()

'''
Created on 2017年5月3日

@author: LokHim
'''
import unittest
import numpy as np
import math
from PIL import Image, ImageDraw
from input_name import URLBASE
from input_ellipse import LOCATION_DICT
from input_image import angleRotate


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
        with Image.open(URLBASE + '/2002/07/30/big/img_997.jpg', 'r') as image:
            ed_list = LOCATION_DICT['2002/07/30/big/img_997']
            for ell_data in ed_list:
                start_x = ell_data.xcoor - ell_data.minor_axis
                start_y = ell_data.ycoor - ell_data.major_axis
                end_x = ell_data.xcoor + ell_data.minor_axis
                end_y = ell_data.ycoor + ell_data.major_axis

                x_0, y_0 = angleRotate(start_x, start_y, ell_data.angle)
                x_1, y_1 = angleRotate(end_x, end_y, ell_data.angle)

                bbox = (x_0, y_0, x_1, y_1)
                print(start_x, start_y, end_x, end_y)
                print(ell_data.angle, bbox)
                draw = ImageDraw.Draw(image)
                draw.rectangle(bbox, outline='red')

            image.show()

    
    @unittest.skip
    def test_draw2(self):
        '''Test case 2 for drawing a ellipse on face image'''

        with Image.open(URLBASE + '/2003/01/17/big/img_377.jpg', 'r') as image:
            ed_list = LOCATION_DICT['2003/01/17/big/img_377']
            for ell_data in ed_list:
                x_0, y_0 = ell_data.xcoor - ell_data.minor_axis, ell_data.ycoor - ell_data.major_axis
                x_1, y_1 = ell_data.xcoor + ell_data.minor_axis, ell_data.ycoor + ell_data.major_axis
                overlay = Image.new(
                    'RGBA', (math.ceil(x_1 - x_0) + 1, math.ceil(y_1 - y_0) + 1))
                draw = ImageDraw.Draw(overlay)
                draw.rectangle(
                    (0, 0, int(x_1 - x_0), int(y_1 - y_0)), outline='red')

                rotated = overlay.rotate(ell_data.angle, expand=True)
                image.paste(rotated, (int(x_0), int(y_0)), rotated)

            image.show()

    #Final Method
    def test_draw3(self):
        '''Test case 3 for drawing a ellipse on face image'''
        with Image.open(URLBASE + '/2002/09/01/big/img_16680.jpg', 'r') as image:
            ed_list = LOCATION_DICT['2002/09/01/big/img_16680']
            for ell_data in ed_list:
                start_x = ell_data.xcoor - ell_data.minor_axis
                start_y = ell_data.ycoor - ell_data.major_axis
                end_x = ell_data.xcoor + ell_data.minor_axis
                end_y = ell_data.ycoor + ell_data.major_axis
                bbox = (start_x, start_y, end_x, end_y)
                
                new = image.rotate(ell_data.angle)
                crop_image = new.crop(bbox)
                crop_image.show()

            
            image.show()
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testImage']
    unittest.main()

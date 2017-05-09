'''
Created on 2017年5月3日

@author: LokHim
'''
import unittest
import math
import numpy as np
from PIL import Image, ImageDraw
from input import *
from input.input_image import angleRotate as ar


class Test(unittest.TestCase):
    
    @unittest.skip
    def testImage(self):
        with Image.open(urlbase + '/2002/08/11/big/img_743.jpg', 'r') as image:
            rgb_image = image.convert('RGB')
            # row first
            r, g, b = rgb_image.getpixel((0, 319))
            arrtest = np.array([r, g, b])

            arr = np.array(image)
            # column first
            pixel = arr[319, 0]
            print(arrtest, pixel, len(arr[0]))

            self.assertTrue((arrtest == pixel).all(), "Not Equal Pixel")

    @unittest.skip
    def testCutting(self):
        with Image.open(urlbase + '/2002/08/26/big/img_265.jpg', 'r') as image:
            ed_list = locationdict['2002/08/26/big/img_265']
            for ed in ed_list:
                x0, y0 = ed.x - ed.minorAxis, ed.y - ed.majorAxis
                x1, y1 = ed.x + ed.minorAxis, ed.y + ed.majorAxis
                bbox = (x0, y0, x1, y1)
                print(ed.angle, bbox)
                draw = ImageDraw.Draw(image)
                draw.ellipse(bbox, outline='red')

            image.show()

    
    def testCutting2(self):
        overlay = Image.new('RGBA', (200, 100))
        draw = ImageDraw.Draw(overlay)
        draw.ellipse((0, 0, 200, 100), '#0f0')
        
        im = Image.new('RGB',(500,500),'#f00')
        rotated = overlay.rotate(45, expand=True)
        im.paste(rotated, (0, 0), rotated)
        im.show()
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testImage']
    unittest.main()

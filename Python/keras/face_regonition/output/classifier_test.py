'''
Created on 2017年6月15日

@author: LokHim
'''
import unittest
from PIL import Image, ImageDraw
from llh.Python.keras.face_regonition.input import URLBASE
from llh.Python.keras.face_regonition.input.input_ellipse import LOCATION_DICT
from llh.Python.keras.face_regonition.input.crop_image import crop, location_of_face
from llh.Python.keras.face_regonition.output.classifier import predict, needMerge


class Test(unittest.TestCase):

    def setUp(self):
        self.filename = '2003/01/15/big/img_1213'
        self.image = Image.open(URLBASE + '/' + self.filename + '.jpg', 'r')

    def tearDown(self):
        self.image.close()

    @unittest.skip
    def testPredict(self):
        croped_list = crop(self.image, (80, 80), 4)
        result_list = predict('12-net-calibration', croped_list, self.image)
        self.assertTrue(len(result_list) > 0, 'List is  null')

    def test_needMerge(self):
        face_list = LOCATION_DICT[self.filename]
        location_set = set()
        draw = ImageDraw.Draw(self.image)
        croped_list = []

        for face in face_list:
            bbox = location_of_face(face)
            draw.rectangle(bbox, outline='green')
            location_set.add(bbox)

        for location in location_set:
            width = location[2] - location[0]
            height = location[3] - location[1]
            # Main Process
            box_list = crop(self.image, (width, height), 4)
            croped_list.extend(predict('12-net', box_list, self.image))

        for rbox in croped_list:
            if any([needMerge(rbox, loc, 0.2) for loc in location_set]):
                draw.rectangle(rbox, outline='red')
            else:
                pass
        self.image.show()

    @unittest.skip
    def test_needMerge2(self):
        self.assertTrue(
            needMerge((1, 1, 10, 10), (0, 0, 11, 11), 0.8), 'needMerge2 Fail!')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

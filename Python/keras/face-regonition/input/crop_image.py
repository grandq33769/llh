'''
Created on 2017年5月3日

@author: LokHim
'''
from PIL import Image
from input_name import FILESET, URLBASE
from input_ellipse import LOCATION_DICT
import numpy as np


def crop_face(face_list, image):
    return_list = []
    for face in face_list:
        start_x = face.xcoor - face.minor_axis
        start_y = face.ycoor - face.major_axis
        end_x = face.xcoor + face.minor_axis
        end_y = face.ycoor + face.major_axis
        bbox = (start_x, start_y, end_x, end_y)

        new = image.rotate(face.angle)
        crop_image = new.crop(bbox)
        return_list.append(crop_image)

    return return_list

total = 0 #5171
for filename in FILESET:
    with Image.open(URLBASE + '/' + filename + '.jpg', 'r') as image:
        face_list = LOCATION_DICT[filename]
        croped_list = crop_face(face_list, image)
        file_name = filename.replace('/','_')
        save_path = URLBASE + '/Input_Data/Positive/' + file_name
        for croped_face in croped_list:
            index = croped_list.index(croped_face)
            str_index = str(index)
            total += 1
            croped_face.save(save_path + '_' + str_index + '.jpg')
            
print(total)

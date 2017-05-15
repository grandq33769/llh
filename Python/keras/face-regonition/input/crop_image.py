'''
Created on 2017年5月3日

@author: LokHim
'''
import os
from itertools import product
from PIL import Image
from input_name import FILESET, URLBASE
from input_ellipse import LOCATION_DICT

PADDING_SIZE = 5
SAMPLE_SIZE = 12


def is_overlap(income, origin):
    '''A function to determine two region is it overlap'''
    origin = [x for x in map(lambda x: int(x + PADDING_SIZE), list(origin))]
    income_x = {x for x in range(income[0], income[2] + 1)}
    income_y = {y for y in range(income[1], income[3] + 1)}
    origin_x = {x for x in range(origin[0], origin[2])}
    origin_y = {y for y in range(origin[1], origin[3])}

    if income_x - origin_x != income_x and income_y - origin_y == income_y:
        return True
    else:
        return False


def location_of_face(face):
    '''return a tuple of face location (top-left and bottom-right) from face object'''
    start_x = face.xcoor - face.minor_axis
    start_y = face.ycoor - face.major_axis
    end_x = face.xcoor + face.minor_axis
    end_y = face.ycoor + face.major_axis
    return (start_x, start_y, end_x, end_y)


def crop_negative(face_list, image, image_size):
    '''A function to crop all negative face samples from a image'''
    return_list = []
    location_list = []
    width, height = image.size

    for face in face_list:
        bbox = location_of_face(face)
        location_list.append(bbox)

    for x_start, y_start in product(range(0, width, image_size), range(0, height, image_size)):
        rbox = [x_start, y_start, x_start +
                image_size, y_start + image_size]
        if any([is_overlap(rbox, loc) for loc in location_list]):
            pass
        else:
            return_list.append(rbox)
    return return_list


def crop_face(face_list, image):
    '''A function to crop all face in an image'''
    return_list = []
    for face in face_list:
        bbox = location_of_face(face)
        new = image.rotate(face.angle)
        crop_image = new.crop(bbox)
        return_list.append(crop_image)

    return return_list


TOTAL = 0  # 5171
# Crop face image
for filename in FILESET:
    with Image.open(URLBASE + '/' + filename + '.jpg', 'r') as image:
        face_list = LOCATION_DICT[filename]
        croped_list = crop_face(face_list, image)
        file_name = filename.replace('/', '_')
        save_path = URLBASE + '/Input_Data/Positive/' + file_name
        for croped_face in croped_list:
            index = croped_list.index(croped_face)
            str_index = str(index)
            croped_face.save(save_path + '_' + str_index + '.jpg')
            TOTAL += 1

print(TOTAL)

# Crop background image
TOTAL = 0
for filename in FILESET:
    with Image.open(URLBASE + '/' + filename + '.jpg', 'r') as image:
        face_list = LOCATION_DICT[filename]
        croped_list = crop_negative(face_list, image, SAMPLE_SIZE)
        file_name = filename.replace('/', '_')
        save_path = URLBASE + '/Input_Data/Negative/'
        for croped_neg in croped_list:
            str_index = str(TOTAL)
            crop_image = image.crop(tuple(croped_neg))
            final_path = save_path + str_index + '.jpg'

            if (not os.path.exists(final_path)):
                crop_image.save(final_path)
            TOTAL += 1
        print(TOTAL)

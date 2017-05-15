'''
Created on 2017年5月3日

@author: LokHim
'''
from math import ceil
from itertools import product
from PIL import Image
from input_name import FILESET, URLBASE
from input_ellipse import LOCATION_DICT

PADDING_SIZE = 5
SAMPLE_SIZE = 12
SPACING = 4


def is_overlap(income, origin):
    origin = [x for x in map(lambda x: int(x + PADDING_SIZE), list(origin))]
    income_x = {x for x in range(income[0], income[2] + 1)}
    income_y = {y for y in range(income[1], income[3] + 1)}
    origin_x = {x for x in range(origin[0], origin[2])}
    origin_y = {y for y in range(origin[1], origin[3])}

    if income_x - origin_x != income_x and income_y - origin_y != income_y:
        return True
    else:
        return False


def location_of_face(face):
    start_x = face.xcoor - face.minor_axis
    start_y = face.ycoor - face.major_axis
    end_x = face.xcoor + face.minor_axis
    end_y = face.ycoor + face.major_axis
    return (int(start_x), int(start_y), ceil(end_x), ceil(end_y))


def crop_negative(face_list, image, image_size):
    return_set = set()
    location_set = set()
    width, height = image.size

    for face in face_list:
        bbox = location_of_face(face)
        location_set.add(bbox)

    for x_start, y_start in product(range(0, width, image_size), range(0, height, image_size)):
        rbox = [x_start, y_start, x_start +
                image_size, y_start + image_size]
        if any([is_overlap(rbox, loc) for loc in location_set]):
            pass
        else:
            return_set.add(rbox)
    return return_set


def crop_face(face_list, image, image_size, spacing):
    return_list = []
    for face in face_list:
        sample_set = set()
        bbox = location_of_face(face)
        new = image.rotate(face.angle)
        for x_start, y_start in product(range(bbox[0], bbox[2], spacing), range(bbox[1], bbox[3], spacing)):
            rbox = (x_start, y_start, x_start +
                    image_size, y_start + image_size)
            sample_set.add(rbox)
        return_list.append(new.crop(rbox) for rbox in sample_set)
    return return_list

total = 0  # 5171
# Crop face image
for filename in FILESET:
    with Image.open(URLBASE + '/' + filename + '.jpg', 'r') as image:
        face_list = LOCATION_DICT[filename]
        croped_list = crop_face(face_list, image, SAMPLE_SIZE, SPACING)
        file_name = filename.replace('/', '_')
        save_path = URLBASE + '/Input_Data/Positive/' + file_name
        for croped_face in croped_list:
            for croped_image in croped_face:
                str_index = '{:04d}'.format(total)
                croped_image.save(save_path + '_' + str_index + '.jpg')
                total += 1

        print('Positive Example: ' + str(total))
POSITIVE_SAMPLE = total

# Crop background image
total = 0
for filename in FILESET:
    with Image.open(URLBASE + '/' + filename + '.jpg', 'r') as image:
        face_list = LOCATION_DICT[filename]
        croped_set = crop_negative(face_list, image, SAMPLE_SIZE)
        file_name = filename.replace('/', '_')
        save_path = URLBASE + '/Input_Data/Negative/'
        for croped_neg in croped_set:
            str_index = str(total)
            crop_image = image.crop(tuple(croped_neg))
            final_path = save_path + str_index + '.jpg'
            crop_image.save(final_path)
            total += 1

        print('Negative Example: ' + str(total))
NEGATIVE_SAMPLE = total

print('Positive samples: ' + POSITIVE_SAMPLE +
      'Negative samples: ' + NEGATIVE_SAMPLE)

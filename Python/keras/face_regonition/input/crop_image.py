'''
Created on 2017年5月3日

@author: LokHim
'''
from math import ceil
from itertools import product
from PIL import Image
from llh.Python.keras.face_regonition.input.input_name import FILESET, URLBASE
from llh.Python.keras.face_regonition.input.input_ellipse import LOCATION_DICT

PADDING_SIZE = 5
SAMPLE_SIZE = 12
SPACING = 4


def transform_bbox(location):
    '''A fucntion to transform class LOCATION to PIL-use data'''
    start_x = location.xcoor - location.minor_axis
    start_y = location.ycoor - location.major_axis
    end_x = location.xcoor + location.minor_axis
    end_y = location.ycoor + location.major_axis
    return (start_x, start_y, end_x, end_y)


def is_overlap(income, origin):
    '''A function to determine two region is it overlap'''
    origin = [x for x in map(lambda x: int(x + PADDING_SIZE), list(origin))]
    income_x = {x for x in range(income[0], income[2] + 1)}
    income_y = {y for y in range(income[1], income[3] + 1)}
    origin_x = {x for x in range(origin[0], origin[2])}
    origin_y = {y for y in range(origin[1], origin[3])}

    return income_x - origin_x != income_x and income_y - origin_y != income_y


def location_of_face(face):
    '''return a tuple of face location (top-left and bottom-right) from face object'''
    start_x = face.xcoor - face.minor_axis
    start_y = face.ycoor - face.major_axis
    end_x = face.xcoor + face.minor_axis
    end_y = face.ycoor + face.major_axis
    return (int(start_x), int(start_y), ceil(end_x), ceil(end_y))


def crop_negative(face_list, image, image_size):
    '''A function to crop all negative face samples from a image'''
    return_set = set()
    location_set = set()
    width, height = image.size

    for face in face_list:
        bbox = location_of_face(face)
        location_set.add(bbox)

    for x_start, y_start in product(range(0, width, image_size), range(0, height, image_size)):
        rbox = (x_start, y_start, x_start +
                image_size, y_start + image_size)
        if any([is_overlap(rbox, loc) for loc in location_set]):
            pass
        else:
            return_set.add(rbox)
    return return_set


def crop_face(face_list, image, image_size, spacing):
    '''A function to crop all face in an image'''
    return_list = []
    for face in face_list:
        sample_set = set()
        bbox = location_of_face(face)
        new_image = image.rotate(face.angle).crop(bbox)
        '''
        for x_start, y_start in product(range(bbox[0], bbox[2], spacing),
                                        range(bbox[1], bbox[3], spacing)):
            rbox = (x_start, y_start, x_start +
                    image_size, y_start + image_size)
            sample_set.add(rbox)
        '''
        return_list.append(new_image)
    return return_list


def crop(image, image_size, spacing):
    '''A function to crop all window in an image'''
    return_set = []
    width, height = image.size
    for x_start, y_start in product(range(0, width-image_size, spacing), range(0, height-image_size, spacing)):
        rbox = (x_start, y_start, x_start +
                image_size, y_start + image_size)
        return_set.append(rbox)
    return return_set


if __name__ == "__main__":
    TOTAL = 0  # 5171
    # Crop face image
    for filename in FILESET:
        with Image.open(URLBASE + '/' + filename + '.jpg', 'r') as img:
            croped_list = crop_face(
                LOCATION_DICT[filename], img, SAMPLE_SIZE, SPACING)
            file_name = filename.replace('/', '_')
            save_path = URLBASE + '/Face/' + file_name
            for croped_face in croped_list:
                #for croped_image in croped_face:
                str_index = '{:04d}'.format(TOTAL)
                croped_face.save(save_path + '_' + str_index + '.jpg')
                TOTAL += 1

            print('Positive Example: ', TOTAL)
    POSITIVE_SAMPLE = TOTAL
    '''
    # Crop background image
    TOTAL = 0
    for filename in FILESET:
        with Image.open(URLBASE + '/' + filename + '.jpg', 'r') as img:
            croped_set = crop_negative(
                LOCATION_DICT[filename], img, SAMPLE_SIZE)
            file_name = filename.replace('/', '_')
            save_path = URLBASE + '/Input_Data/Negative/'
            for croped_neg in croped_set:
                crop_image = img.crop(tuple(croped_neg))
                crop_image.save(save_path, TOTAL, '.jpg')
                TOTAL += 1

            print('Negative Example: ', TOTAL)
    '''
            
    NEGATIVE_SAMPLE = TOTAL
    print('Positive samples: ', POSITIVE_SAMPLE,
          'Negative samples: ', NEGATIVE_SAMPLE)

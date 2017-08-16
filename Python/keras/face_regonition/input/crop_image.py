'''
Created on 2017年5月3日

@author: LokHim
'''
import os
import tensorflow as tf
import gc
import glob
import time
import multiprocessing as mp
from math import ceil
from itertools import product
from PIL import Image
from llh.Python.keras.face_regonition.input.input_name import FILESET, URLBASE
from llh.Python.keras.face_regonition.input.input_ellipse import LOCATION_DICT
from llh.Python.keras.face_regonition.output import MODEL_LIST

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
PADDING_SIZE = 5


def setOfIntersection(income, origin):
    income_x = {x for x in range(income[0], income[2] + 1)}
    income_y = {y for y in range(income[1], income[3] + 1)}
    origin_x = {x for x in range(origin[0], origin[2])}
    origin_y = {y for y in range(origin[1], origin[3])}
    return income_x, income_y, origin_x, origin_y


def is_overlap(income, origin):
    '''A function to determine two region is it overlap'''
    origin = [x for x in map(lambda x: int(x + PADDING_SIZE), list(origin))]
    income_x, income_y, origin_x, origin_y = setOfIntersection(income, origin)
    return income_x - origin_x != income_x and income_y - origin_y != income_y


def location_of_face(face):
    '''return a tuple of face location (top-left and bottom-right) from face object'''
    start_x = face.xcoor - face.minor_axis
    start_y = face.ycoor - face.major_axis
    end_x = face.xcoor + face.minor_axis
    end_y = face.ycoor + face.major_axis
    return (int(start_x), int(start_y), ceil(end_x), ceil(end_y))


def cropResult(face_list, image, name):
    from llh.Python.keras.face_regonition.output.classifier import predict, needMerge
    #return_list[0] = positive ; return_list[1] = negative
    return_list = [[], []]
    location_set = set()
    croped_list = []

    for face in face_list:
        bbox = location_of_face(face)
        location_set.add(bbox)

    model = MODEL_LIST[MODEL_LIST.index(name) - 1]
    for location in location_set:
        width = location[2] - location[0]
        height = location[3] - location[1]
        # Main Process
        box_list = crop(image, (width, height), 4)
        croped_list.extend(predict(model, box_list, image))

    for rbox in croped_list:
        croped_image = image.crop(rbox)
        if any([needMerge(rbox, loc, 0.5) for loc in location_set]):
            return_list[0].append(croped_image)
        else:
            return_list[1].append(croped_image)

    return return_list


def crop_negative(face_list, image):
    '''A function to crop all negative face samples from a image'''
    return_list = []
    location_set = set()
    size_list = []
    width, height = image.size

    for face in face_list:
        bbox = location_of_face(face)
        location_set.add(bbox)

    for location in location_set:
        swidth = location[2] - location[0]
        sheight = location[3] - location[1]
        size_list.append([swidth, sheight])

    for size in size_list:
        for x_start, y_start in product(range(0, width, size[0]), range(0, height, size[1])):
            rbox = (x_start, y_start, x_start +
                    size[0], y_start + size[1])
            if any([is_overlap(rbox, loc) for loc in location_set]):
                pass
            else:
                croped_image = image.crop(rbox)
                return_list.append(croped_image)
    return return_list


def crop_face(face_list, image):
    '''A function to crop all face in an image'''
    return_list = []
    for face in face_list:
        bbox = location_of_face(face)
        new_image = image.rotate(face.angle).crop(bbox)
        return_list.append(new_image)
    return return_list


def crop(image, image_size, spacing):
    '''A function to crop all window in an image'''
    return_set = []
    width, height = image.size
    for x_start, y_start in product(range(0, width - image_size[0], spacing), range(0, height - image_size[1], spacing)):
        rbox = (x_start, y_start, x_start +
                image_size[0], y_start + image_size[1])
        return_set.append(rbox)
    return return_set


def processImage(name, filename, function, path_str, total_crop):
    start_time = time.time()

    total_list = [[], []]
    with Image.open(URLBASE + '/' + filename + '.jpg', 'r') as img:
        if function.__name__ == 'cropResult':
            total_list = function(LOCATION_DICT[filename], img, name)

        elif function.__name__ == 'crop_face':
            total_list[0] = function(LOCATION_DICT[filename], img)

        elif function.__name__ == 'crop_negative':
            total_list[1] = function(LOCATION_DICT[filename], img)
        else:
            raise NameError

        file_index = 1
        for index, croped_list in enumerate(total_list):
            if(len(croped_list) > 0):
                for croped_face in croped_list:
                    croped_face.save(
                        path_str[index] + '_' + str(file_index) + '.jpg')
                    file_index += 1
                    total_crop.value += 1

        total_time = time.time() - start_time
        print(
            filename, 'Process Finished. Processing Time: {:.3f} sec'.format(total_time))


def saveImage(name, function):
    '''A function can crop Positive/Negative image and save to specific path'''
    total = 0
    total_crop = mp.Value('i', 0)
    for filename in FILESET:
        print('\nProcessing : ', filename,
              'Number of Image Processed : ', total)
        file_name = filename.replace('/', '_')
        save_path = [URLBASE + '/Input_Data/' + name + '/Positive/' + file_name,
                     URLBASE + '/Input_Data/' + name + '/Negative/' + file_name]
        total += 1

        # Determine image has been processed
        break_flag = False
        path_str = []
        if function.__name__ == 'cropResult':
            path_str = [path.replace('_big', '') for path in save_path]
        else:
            path_str = save_path

        for path in path_str:
            if(glob.glob(path + '_*') != []):
                print(function.__name__, filename, 'had already processed...')
                break_flag = True
                break
        if(break_flag == True):
            continue

        # Process Begin
        else:
            process = mp.Process(target=processImage, args=(
                name, filename, function, path_str, total_crop,))
            process.start()
            process.join()

    print('Number of Cropped Image Save: ', total_crop.value)


if __name__ == "__main__":
    # Total Faces: 5171
    #saveImage('12-net-calibration', crop_face)
    saveImage('12-net', crop_negative)

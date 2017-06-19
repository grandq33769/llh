'''
Created on 2017年6月15日

@author: LokHim
'''
import gc
import time
import numpy as np
from math import ceil, sqrt
from itertools import product, combinations
from keras.models import load_model
from llh.Python.keras.face_regonition.input import URLBASE
from llh.Python.keras.face_regonition.input.input_image import transform
from llh.Python.keras.face_regonition.input.crop_image import setOfIntersection, is_overlap
from llh.Python.keras.face_regonition.output import MODEL_LIST

S_LIST = [0.83, 0.91, 1.0, 1.10, 1.21]
X_LIST = [-0.17, 0, 0.17]
Y_LIST = [-0.17, 0, 0.17]
THRESHOLD = {'12-net': 0.999, '12-net-calibration': 0.999}
NMS_THRESHOLD = {'12-net-calibration': 0.9}


def predict(name, box_list, image):
    now_index = MODEL_LIST.index(name)
    model = load_model(URLBASE + '/Model/' + name + '.h5')
    input_size = int(name[:2])
    threshold = THRESHOLD[name]
    return_list = []
    # Recursive
    if(now_index != 0):
        blist = predict(MODEL_LIST[now_index - 1], box_list, image)
        start_time = time.time()
        if(now_index % 2 == 0):
            return_list = getResult(model, threshold, image, blist, input_size)
        else:
            for box in blist:
                return_list.append(getCalResult(
                    model, threshold, image, box, input_size))
            return_list = suppression(return_list, NMS_THRESHOLD[name])

    else:
        blist = box_list
        start_time = time.time()
        return_list = getResult(model, threshold, image, blist, input_size)

    total_time = time.time() - start_time
    print('End of', name, '...... Processing Time : {:.3f} sec'.format(total_time))
    return return_list


def getResult(model, threshold, image, blist, input_size):
    x_train = np.empty(shape=(len(blist), input_size, input_size, 3))
    for index, box in enumerate(blist):
        crop_image = image.crop(box)
        x_train[index] = transform(crop_image, (input_size, input_size, 3))

    output = model.predict(x_train)
    return_list = []
    for index, result in enumerate(output):
        if result[1] > threshold:
            return_list.append(blist[index])

    del x_train
    gc.collect()
    return return_list


def getCalResult(model, threshold, image, box, input_size):
    cbox_list = [[s, x, y] for s, x, y in product(S_LIST, X_LIST, Y_LIST)]
    x_train = np.empty(shape=(len(cbox_list), input_size, input_size, 3))
    for index, cbox in enumerate(cbox_list):
        crop_image = image.crop(calibrationTransform(box, cbox))
        x_train[index] = transform(crop_image, (input_size, input_size, 3))

    output = model.predict(x_train)
    result_list = []
    for index, result in enumerate(output):
        if result[1] > threshold:
            result_list.append(cbox_list[index])

    if(result_list != []):
        result = calibrationTransform(box, tuple(
            sum(i) / len(result_list) for i in zip(*result_list)))
    else:
        result = box

    del x_train, cbox_list
    gc.collect()
    return result


def calibrationTransform(bbox, cbox):
    height = bbox[3] - bbox[1]
    width = bbox[2] - bbox[0]
    start_x = bbox[0] - ((cbox[1] * width) / cbox[0])
    start_y = bbox[1] - ((cbox[2] * height) / cbox[0])
    end_x = start_x + (width / cbox[0])
    end_y = start_y + (height / cbox[0])
    return (int(start_x), int(start_y), ceil(end_x), ceil(end_y))


def needMerge(first, second, threshold):
    if (is_overlap(first, second)):
        income_x, income_y, origin_x, origin_y = setOfIntersection(
            first, second)
        intersection = len(income_x & origin_x) * len(income_y & origin_y)
        total = len(income_x) * len(income_y) + \
            len(origin_x) * len(origin_y) - intersection
        if (intersection / total) > threshold:
            return True
        else:
            return False
    else:
        return False


def merge(first, second):
    value = []
    for x in range(0, 4):
        if(x < 2):
            if (first[x] < second[x]):
                value.append(first[x])
            else:
                value.append(second[x])
        else:
            if (first[x] > second[x]):
                value.append(first[x])
            else:
                value.append(second[x])
    return tuple(value)


def suppression(blist, threshold):
    return_list = blist
    flag = True
    while(flag):
        time = 0
        for com_list in combinations(return_list, 2):
            time += 1
            if(needMerge(com_list[0], com_list[1], threshold)):
                return_list.remove(com_list[0])
                return_list.remove(com_list[1])
                return_list.append(merge(com_list[0], com_list[1]))
                break
        if(time == len(list(combinations(return_list, 2)))):
            flag = False

    return return_list

'''
Created on 2017年4月12日

@author: LokHim
'''
from llh.Python.regression.housing.data_input import TARGET_LIST

WEIGHT = -2.3272
WEIGHT_2 = 0.0434
BIAS = 42.8169
LEARNING_RATE = 0.0000000195
STEP = 200000


def predict(input_attr):
    '''Function for prediction'''
    return WEIGHT * input_attr + WEIGHT_2 * input_attr**2 + BIAS


def loss(input_attr, target):
    '''Function for calculating loss'''
    return (target - predict(input_attr))**2


def differential_of_weight(input_attr, target):
    '''Function for calculating gradient of weight 1'''
    return -2 * (target - predict(input_attr)) * (input_attr)


def differential_of_weight2(input_attr, target):
    '''Function for calculating gradient of weight 2'''
    return -2 * (target - predict(input_attr)) * (input_attr)**2


def differential_of_bias(input_attr, target):
    '''Function for calculating gradient of bias'''
    return -2 * (target - predict(input_attr))


def optimize(sum_of_db, sum_of_dw, sum_of_dw2):
    '''Function for update the parameter'''
    global WEIGHT, WEIGHT_2, BIAS, LEARNING_RATE
    WEIGHT = WEIGHT - LEARNING_RATE * sum_of_dw
    WEIGHT_2 = WEIGHT_2 - LEARNING_RATE * sum_of_dw2
    BIAS = BIAS - LEARNING_RATE * sum_of_db


for i in range(0, STEP):
    dw = dw2 = db = loss = 0

    for member in TARGET_LIST:
        # print(predict(member[0]),member[1])
        dw += differential_of_weight(member[0], member[1])
        dw2 += differential_of_weight2(member[0], member[1])
        db += differential_of_bias(member[0], member[1])
        loss += loss(member[0], member[1])

    optimize(db, dw, dw2)
    print("Step :", '{:5d}'.format(i + 1), "  loss: ", '{:-.4f}'.format(loss), "weight:",
          '{:-.4f}'.format(WEIGHT), "weight2:", '{:-.4f}'.format(WEIGHT_2),
          "bias: ", '{:-.4f}'.format(BIAS))

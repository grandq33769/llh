'''
Created on 2017年4月12日

@author: LokHim
'''
from llh.Python.regression.housing.data_input import TARGET_LIST
WEIGHT = 1
BIAS = 1
LEARNING_RATE = 0.000009


def predict(input_attr):
    '''Function for predicting the target by input attribute'''
    return WEIGHT * input_attr + BIAS


def loss(input_attr, target):
    '''Function for calculating the loss of function'''
    return (target - predict(input_attr))**2


def differential_of_weight(input_attr, target):
    '''Function for calculating the gradient of weight'''
    return -2 * (target - predict(input_attr)) * (input_attr)


def differential_of_bias(input_attr, target):
    '''Function for calculating the gradient of bias'''
    return -2 * (target - predict(input_attr))


def optimize(sum_of_db, sum_of_dw):
    '''Function for update the parameter'''
    global WEIGHT, BIAS, LEARNING_RATE
    WEIGHT = WEIGHT - LEARNING_RATE * sum_of_dw
    BIAS = BIAS - LEARNING_RATE * sum_of_db


for i in range(0, 100000):
    dw = 0
    db = 0
    loss = 0
    for member in TARGET_LIST:
        # print(predict(member[0]),member[1])
        dw += differential_of_weight(member[0], member[1])
        db += differential_of_bias(member[0], member[1])
        loss += loss(member[0], member[1])
    optimize(db, dw)
    print("Step ", i + 1, "  loss: ", loss, "weight:", WEIGHT, "bias: ", BIAS)

'''
Created on 2017年4月12日

@author: LokHim
'''
from housing import data_input as di

weight = -2.3272
weight_2 = 0.0434
bias = 42.8169
learning_rate = 0.0000000195
step_of_training = 200000


def predict(input):
    global weight, bias
    return weight * input + weight_2 * input**2 + bias


def loss(input, target):
    return (target - predict(input))**2


def differential_of_weight(input, target):
    return -2 * (target - predict(input)) * (input)


def differential_of_weight2(input, target):
    return -2 * (target - predict(input)) * (input)**2


def differential_of_bias(input, target):
    return -2 * (target - predict(input))


def optimize(sum_of_db, sum_of_dw, sum_of_dw2):
    global weight, weight_2, bias, learning_rate
    weight = weight - learning_rate * sum_of_dw
    weight_2 = weight_2 - learning_rate * sum_of_dw2
    bias = bias - learning_rate * sum_of_db


for i in range(0, step_of_training):
    sum_of_dw = 0
    sum_of_dw2 = 0
    sum_of_db = 0
    sum_of_loss = 0

    for member in di.target_list:
        # print(predict(member[0]),member[1])
        sum_of_dw += differential_of_weight(member[0], member[1])
        sum_of_dw2 += differential_of_weight2(member[0], member[1])
        sum_of_db += differential_of_bias(member[0], member[1])
        sum_of_loss += loss(member[0], member[1])

    optimize(sum_of_db, sum_of_dw, sum_of_dw2)
    print("Step :", '{:5d}'.format(i + 1), "  loss: ", '{:-.4f}'.format(sum_of_loss), "weight:",
          '{:-.4f}'.format(weight), "weight2:", '{:-.4f}'.format(weight_2), "bias: ", '{:-.4f}'.format(bias))

'''
Created on 2017年4月12日

@author: LokHim
'''
import data_input as di
weight = 1
bias = 1
learning_rate = 0.000009


def predict(input):
    global weight, bias
    return weight * input + bias


def loss(input, target):
    return (target - predict(input))**2


def differential_of_weight(input, target):
    return -2 * (target - predict(input)) * (input)


def differential_of_bias(input, target):
    return -2 * (target - predict(input))


def optimize(sum_of_db, sum_of_dw):
    global weight, bias, learning_rate
    weight = weight - learning_rate * sum_of_dw
    bias = bias - learning_rate * sum_of_db

for i in range(0,100000):
    sum_of_dw = 0
    sum_of_db = 0
    sum_of_loss = 0
    for member in di.target_list:
        #print(predict(member[0]),member[1])
        sum_of_dw+= differential_of_weight(member[0], member[1])
        sum_of_db+= differential_of_bias(member[0], member[1])
        sum_of_loss+= loss(member[0], member[1])
    optimize(sum_of_db, sum_of_dw)
    print("Step ",i+1,"  loss: ",sum_of_loss,"weight:",weight,"bias: ", bias)

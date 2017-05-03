'''
Created on 2017年4月27日

@author: LokHim
'''
import matplotlib.pyplot as plt
from collections import OrderedDict

color_list = ['k','r','y','g','m','b','saddlebrown','grey','aquamarine','darkviolet']

def plot(array,labels,ran_list):
    for index,pt in enumerate(array) :
        color_index = labels[ran_list[index]]
        plt.scatter(pt[0], pt[1], color=color_list[color_index], label = str(color_index))
       
    handles, labels = plt.gca().get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.show()
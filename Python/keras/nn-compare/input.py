'''
Created on 2017年4月27日

@author: LokHim
'''

from mnist import MNIST
import random

class DataInputter():
    def __init__(self,mnistPath):
        self.mnistPath = mnistPath
        self.mndata = MNIST(self.mnistPath)

    def get_training_data_and_labels(self):
        return self.mndata.load_training()
    
    def get_testing_data_and_labels(self):
        return self.mndata.load_testing()


if __name__ == '__main__':
    #Verify Mnist Path and the file name should like 'train-labels-idx1-ubyte'
    test = DataInputter('D:/Ecllipse/my-code/Python/keras/nn-compare/mnist-data')
    images, labels = test.get_training_data_and_labels()
    
    index = random.randrange(0, len(images))
    print(test.mndata.display(images[index]))
    print(labels[index])

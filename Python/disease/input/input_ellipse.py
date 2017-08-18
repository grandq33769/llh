'''
Created on 2017年5月4日

@author: LokHim
'''
from .input_name import URLBASE
LOCATION_DICT = dict()


class Location:
    '''A class for saving face data'''

    def __init__(self, *arg):
        self.major_axis = arg[0]
        self.minor_axis = arg[1]
        self.angle = arg[2]
        self.xcoor = arg[3]
        self.ycoor = arg[4]


def read_location(number, data):
    '''Read face location data'''
    locationlist = []
    for _ in range(number):
        dataline = data.readline()[:-4]
        attribute = [float(x) for x in dataline.split(' ')]
        loc = Location(*attribute)
        locationlist.append(loc)
    return locationlist


for i in range(1, 11):
    with open(URLBASE + '/FDDB-folds/FDDB-fold-' + '{:02d}'.format(i)
              + '-ellipseList.txt', 'r') as ellipselist:
        #print('Importing: FDDB-fold-' + '{:02d}'.format(i) + '-ellipseList.txt')
        for line in ellipselist:
            key = line[:-1]
            num = ellipselist.readline()
            returnlist = read_location(int(num), ellipselist)
            LOCATION_DICT.update({key: returnlist})

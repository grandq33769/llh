'''
Created on 2017年5月4日

@author: LokHim
'''
from input import *

class location:
    def __init__(self,*arg):
        self.majorAxis = arg[0]
        self.minorAxis = arg[1]
        self.angle = arg[2]
        self.x = arg[3]
        self.y = arg[4]

def readLocation(num,data):
    locationlist = []
    for i in range(num): 
        line = data.readline()[:-4]
        attribute = [float(x) for x in line.split(' ')]
        l = location(*attribute)
        locationlist.append(l)
    return locationlist

for i in range(1, 11):
    with open(urlbase + '/FDDB-folds/FDDB-fold-' + '{:02d}'.format(i) + '-ellipseList.txt', 'r') as ellipselist:
        print('Importing: FDDB-fold-' + '{:02d}'.format(i) + '-ellipseList.txt')
        for line in ellipselist:
            key = line[:-1]
            num = ellipselist.readline()
            locationlist = readLocation(int(num), ellipselist)
            locationdict.update({key:locationlist})
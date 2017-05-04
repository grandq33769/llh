'''
Created on 2017年5月3日

@author: LokHim
'''
from input import *

for i in range(1, 11):
    with open(urlbase + '/FDDB-folds/FDDB-fold-' +
                   '{:02d}'.format(i) + '.txt', 'r') as nametxt:
        print('Importing: FDDB-fold-' +
                   '{:02d}'.format(i) + '.txt')
        filelist.append(nametxt.read().split('\n'))
        
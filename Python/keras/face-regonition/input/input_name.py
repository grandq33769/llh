'''
Created on 2017年5月3日

@author: LokHim
'''

URLBASE = '/Users/lhleung/Documents/Data/FDDB'
FILESET = set()

for i in range(1, 11):
    with open(URLBASE + '/FDDB-folds/FDDB-fold-' + '{:02d}'.format(i) + '.txt', 'r') as nametxt:
        print('Importing: FDDB-fold-' + '{:02d}'.format(i) + '.txt')
        namelist = nametxt.read().split('\n')
        namelist = [x for x in namelist if len(x) > 0]
        for name in namelist:
            FILESET.add(name)

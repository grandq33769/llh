'''Arrange all location in a month'''
from open_data import RAWDATA, ARRANGE_DICT
ARRANGE_LIST = []


def dict_of_location(alist):
    '''Return dict of location name and number'''
    location = {}
    for ldata in alist:
        if ldata.location in location:
            location[ldata.location] += ldata.number
        else:
            new_dict = {ldata.location:ldata.number}
            location.update(new_dict)

    return location


for data in RAWDATA:
    key = str(data.year) + "/" + str(data.month)
    if key in ARRANGE_DICT:
        ARRANGE_DICT[key].add(data)
    else:
        newset = set()
        newset.add(data)
        newdict = {key: newset}
        ARRANGE_DICT.update(newdict)

for year in range(2003, 2017):
    for month in range(1, 13):
        s = str(year) + '/' + str(month)
        if s in ARRANGE_DICT:
            loc_dict = dict_of_location(ARRANGE_DICT[s])
            ARRANGE_LIST.append(loc_dict)

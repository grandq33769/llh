"""Import raw data"""
from llh.Python.disease import PATH
RAWDATA = set()


class Data():
    """A Class for a tuple of data"""

    def __init__(self, year, month, location, number):
        try:
            self.year = int(year)
        except ValueError:
            self.year = int(year[-4:])

        self.month = int(month)
        self.location = location
        self.number = int(number)

    def __str__(self):
        '''return the string of data information'''

        return "Year:{} Month:{:2} Location:{} Number:{}"\
            .format(self.year, self.month, self.location, self.number)


with open(PATH, encoding='utf-8') as file:
    RAWLIST = file.read().split('\n')
    NUM = 1
    for line in RAWLIST:
        NUM += 1
        datalist = line.split(',')
        data = Data(datalist[0], datalist[1], datalist[2], datalist[7])
        RAWDATA.add(data)

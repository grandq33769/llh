"""Import raw data"""
import os
import datetime
BASE_URL = os.path.dirname(__file__)
PATH = BASE_URL + '/data/influenza_2.csv'
RAWDATA = set()


class Data():
    """A Class for a tuple of data"""

    def __init__(self, year, month, location, number):
        self.year = int(year)
        self.month = int(month)
        self.location = location
        self.number = int(number)

    def __str__(self):
        '''return the string of data information'''

        return "Year:{} Month:{:2} Location:{} Number:{}"\
            .format(self.year, self.month, self.location, self.number)


with open(PATH, encoding='utf-8') as file:
    wflag = False
    RAWLIST = file.read().split('\n')
    for line in RAWLIST:
        lstr = line.encode('utf-8')
        print(lstr)
        datalist = line.split(',')
        if(len(datalist) == 8):
            if(int(datalist[1]) > 12):
                wflag = True
                break

    for line in RAWLIST:
        datalist = line.split(',')
        if(len(datalist) == 8):
            # Process the year to be normalized
            try:
                year = int(datalist[0])
            except ValueError:
                year = int(datalist[0][-4:])

            if(wflag == True):
                temp_date = str(year) + '-W' + datalist[1].zfill(2)
                # convert week in year to month
                month = datetime.datetime.strptime(
                    temp_date + '-0', "%Y-W%W-%w").month

            else:
                month = datalist[1]

            data = Data(year, month, datalist[2], datalist[7])
            RAWDATA.add(data)

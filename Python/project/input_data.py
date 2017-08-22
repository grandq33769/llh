'''
Input word csv
'''

import csv
import re
from llh.Python.project import DPATH

FILE_PATH = DPATH + '/校園友善問卷資料_文字.csv'
QUESTION = 5


def data():
    '''
    Input word csv
    Return: Dict{sid: ans_dict}
    '''
    sdict = {}
    with open(FILE_PATH, 'r', encoding='utf-8') as csvfile:
        raw = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in raw:
            if re.match("[0-9]+[-]*[0-9]*", row[0]):
                tdict = dict()
                cflag = True
                for i in range(QUESTION):
                    ans = str(row[i + 1])
                    if re.search("[\u4e00-\u9fff]+|[0-9]+", ans) is not None:
                        # Match Question No and Answer to Dictionary
                        tdict.update({i + 1: ans})
                    elif ans == '' or ans == 'X':
                        tdict.update({i + 1: "無"})
                    else:
                        print(row[0], ans)
                        cflag = False
                        break
                if cflag:
                    sdict.update({str(row[0]): tdict})

    print('Number of Student:', len(sdict))
    return sdict


if __name__ == '__main__':
    data()

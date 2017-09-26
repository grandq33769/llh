'''
Input word csv
'''

import csv
import re
import pickle
from llh.Python.project.questionnaire import DPATH, PPATH

RAW_PATH = DPATH + '/校園友善問卷資料(全).csv'
WORD_PATH = DPATH + '/校園友善問卷資料_文字.csv'
SIM_PATH = DPATH + '/結果/csv/校園友善問卷資料_文字_結果(Sim).csv'
QUESTION = 5


def word():
    '''
    Input word csv
    Return: Dict{sid: ans_dict}
    '''
    sdict = {}
    with open(WORD_PATH, 'r', encoding='utf-8') as csvfile:
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


def word_cluster(num_cluster):
    '''
    Import every word cluster in different number of cluster
    Return: wlist[word], result[KMeans]
    '''
    from llh.Python.project.questionnaire.cluster import cluster
    try:
        with open(PPATH + '/word_cluster(' + str(num_cluster) + ').pickle', 'rb') as variable:
            wlist, result = pickle.load(variable)
            return wlist, result

    except FileNotFoundError:
        return cluster(num_cluster)


def word_sim():
    '''
    Import all similar word of a student
    Return: Dict{sid:set[word]}
    '''
    sdict = dict()
    with open(SIM_PATH, 'r', encoding='utf-8') as csvfile:
        raw = csv.reader(csvfile, delimiter=',', quotechar='|')
        wset = set()
        for row in raw:
            # print(row[2:8])
            if row[0] is not '':
                sid = row[0].strip()
                wset = set()
            slist = list(filter(None, row[2:8]))
            wset.update(slist)
            sdict.update({sid: wset})
    return sdict


def raw_data():
    '''
    Import raw data to dict
    Return: Dict{sid:list[data]}
    '''
    sdict = dict()
    with open(RAW_PATH, 'r', encoding='utf-8') as csvfile:
        raw = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(raw)
        for row in raw:
            # print(row[:24])
            if row[1] is not '':
                dlist = [row[1]]

                # Age handling
                try:
                    age = int(row[2])
                    if age not in range(18, 22):
                        dlist.append('23 or older')
                    else:
                        dlist.append(str(age))
                except ValueError:
                    dlist.append('23 or older')

                # College handling
                college = row[3].replace('學', '').replace(
                    '院', '').replace('所', '').replace('設計規劃', '規設').replace('規劃與設計', '規設')
                if '管' in college and len(college) is 1:
                    college += '理'
                dlist.append(college)

                # Year handling
                year = ydict(row[5])
                dlist.append(year)

                # Result handling
                try:
                    result = int(row[6])
                    if result <= 60:
                        result = 'Equal or below 60'
                    elif result > 60 and result <= 70:
                        result = '60.01-70'
                    elif result > 70 and result <= 80:
                        result = '70.01-80'
                    elif result > 80 and result <= 90:
                        result = '80.01-90'
                    else:
                        result = 'Greater than 90'
                except ValueError:
                    result = 'NaN'
                dlist.append(result)

                # Location handling
                location = row[7]
                if re.match('.*縣|.*市', location):
                    location = location.replace('縣', '').replace('市', '')
                elif location is '' or len(location) is 1:
                    location = 'NaN'
                dlist.append(location)

                # Rest of answer handling (Number)
                for qno in range(8, 24):
                    ans = str(qno) + ':'
                    if row[qno] is not '':
                        ans += row[qno]
                    else:
                        ans += 'NaN'
                    dlist.append(ans)
                # print(dlist)
                sid = row[0].strip()
                sdict.update({sid: dlist})
    return sdict


def ydict(year):
    '''Dictionary for indexing year'''
    return{
        '1': '一',
        '2': '二',
        '3': '三',
        '4': '四',
        '一': '一',
        '二': '二',
        '三': '三',
        '四': '四'
    }.get(year, 'NaN')


if __name__ == '__main__':
    word_cluster(11)

'''
Output the result of questionair
'''
import csv
import pickle
from llh.Python.project import CPATH
from llh.Python.project.word_vector import word2vec

NUM_ATT = 5
NOLIST = [str(n + 1) for n in range(222)]  # Data 序列 1 ~ 222
NOLIST2 = ['2-' + str(n + 1) for n in range(331)]  # Data 序列 2-1 ~ 2-331
IDLIST = NOLIST + NOLIST


def write_cluster():
    '''
    Output the result of Clustering
    '''
    outlist = list()
    with open(CPATH + '/word_result.pickle', 'rb') as variable:
        wlist, allresult = pickle.load(variable)
        for cno, word in enumerate(wlist):
            templist = list()
            templist.append(word)
            templist.extend([allresult[x].labels_[cno] for x in range(10, 41)])
            outlist.append(templist)

    with open(CPATH + '/校園友善問卷資料_文字_Cluster.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in outlist:
            writer.writerow(row)


def write_keyword():
    '''
    Output the result of Keyword
    '''
    sdict, _ = word2vec()
    with open('校園友善問卷資料_文字_結果(KeyWord).csv', 'w') as file:
        file.write("ID,1,2,3,4,5\n")
        for sid in IDLIST:
            line = sid + ','
            try:
                ans_dict = sdict[sid]
            except KeyError:
                continue

            for _, word_dict in ans_dict.items():
                ans_line = str()
                for word in word_dict:
                    ans_line += word + ' '
                ans_line = ans_line[:-1] + ','
                line += ans_line
            line = line[:-1] + '\n'
            file.write(line)


def write_absent():
    '''
    Output the result of absent word
    '''
    _, null = word2vec()
    with open('Absent Word.txt', 'w') as file:
        line = str()
        for word in null:
            line += word + ','
        line = line[:-1]
        file.write(line)


def write_word2vec():
    '''
    Output the result of word2vec
    '''
    sdict, _ = word2vec()
    with open('校園友善問卷資料_文字_結果(Sim).csv', 'w', encoding='utf-8') as file:
        firstline = "ID,QNo,Word,"
        numlist = [n + 1 for n in range(NUM_ATT)]
        for num in numlist:
            firstline += str(num) + ','
        firstline = firstline[:-1] + '\n'
        file.write(firstline)

        for sid in IDLIST:
            qflag = True
            line = sid + ','
            try:
                ans_dict = sdict[sid]
            except KeyError:
                continue

            for qno, word_dict in ans_dict.items():
                wflag = True
                if qflag:
                    line += str(qno) + ','
                else:
                    line = ',' + str(qno) + ','

                for word, arr in word_dict.items():
                    if wflag:
                        line += word + ','
                    else:
                        line = ',,' + word + ','

                    if isinstance(arr, int):
                        line += str(arr) + ','
                    else:
                        for value in arr:
                            line += str(value) + ','

                    line = line[:-1] + '\n'
                    print(line)
                    file.write(line)
                    wflag = False
                qflag = False


if __name__ == '__main__':
    write_absent()

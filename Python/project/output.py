'''Output the result of questionair'''
from llh.Python.project.word_vector import SDICT, NULL_SET

NUM_ATT = 5
nolist = [str(n + 1) for n in range(222)]  # Data 序列 1 ~ 222
nolist2 = ['2-' + str(n + 1) for n in range(331)]  # Data 序列 2-1 ~ 2-331
mergelist = nolist + nolist2

with open('校園友善問卷資料_文字_結果(KeyWord).csv', 'w') as file:
    file.write("ID,1,2,3,4,5\n")
    for sid in mergelist:
        line = sid + ','
        try:
            ans_dict = SDICT[sid]
        except KeyError:
            continue

        for qno, word_dict in ans_dict.items():
            ans_line = str()
            for word in word_dict:
                ans_line += word + ' '
            ans_line = ans_line[:-1] + ','
            line += ans_line
        line = line[:-1] + '\n'
        file.write(line)

with open('Absent Word.txt', 'w') as file:
    line = str()
    for word in NULL_SET:
        line += word + ','
    line = line[:-1]
    file.write(line)

with open('校園友善問卷資料_文字_結果(Sim).csv', 'w', encoding='utf-8') as file:
    firstline = "ID,QNo,Word,"
    numlist = [n + 1 for n in range(len(SDICT['1'][1]))]
    for num in numlist:
        firstline += str(num) + ','
    firstline = firstline[:-1] + '\n'
    file.write(firstline)

    for sid in mergelist:
        new_Qflag = True
        line = sid + ','
        try:
            ans_dict = SDICT[sid]
        except KeyError:
            continue

        for qno, word_dict in ans_dict.items():
            new_Wflag = True
            if new_Qflag:
                line += str(qno) + ','
            else:
                line = ',' + str(qno) + ','

            for word, arr in word_dict.items():
                if new_Wflag:
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
                new_Wflag = False
            new_Qflag = False

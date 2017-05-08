'''Output the result of Frequent ItemSet'''
import csv
from mining import RESULT_DICT

with open('FrequentItemSet.csv', 'w', newline='', encoding='utf-8') as file:
    CWRITER = csv.writer(file, delimiter=' ')
    for member in RESULT_DICT:
        line = str()
        for name in member:
            line += str(name) + ','
        line += str(RESULT_DICT[member][0]) + ','
        line += str(RESULT_DICT[member][1])
        CWRITER.writerow(line)

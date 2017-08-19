"""To import birth data"""

import os
import csv

BASE_URL = os.path.dirname(__file__)
print(BASE_URL)
PATH = BASE_URL + '/Birth_Rate.csv'

with open(PATH, encoding='utf-8', newline='\n') as csvfile:
    RAW = csvfile.read()
    print(RAW)

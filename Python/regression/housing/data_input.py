'''
Created on 2017年4月12日

@author: LokHim
'''
from _io import open

#Meta-data
file_name = 'housing_data.txt'
attribute_name =['CRIM','ZN','INDUS','CHAS','NOX','RM','AGE','DIS','RAD','TAX','PTRATIO','B','LSTAT','MEDV']
input_attribute_index = 12
target_attribute_index = 13
number_of_tuple = 506
target_list = []

# Input file
with open(file_name, 'r') as file:
    for line in file:
        # Split up from line to attribute and append to target_list
        member = line[:-2].split(' ')
        member = list(filter(None, member))
        member = [float(attribute) for attribute in member]
        target_list.append((member[input_attribute_index], member[target_attribute_index]))
if target_list.__len__() != number_of_tuple :
    raise Exception('Number of tuple in target list isn\'t correct to '+str(number_of_tuple))
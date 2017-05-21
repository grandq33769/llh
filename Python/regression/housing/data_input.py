'''Module for inputting raw data to a list'''
from llh.Python.regression.housing \
    import BASE_URL, FILE_NAME, INPUT_INDEX, TARGET_INDEX, NUM_OF_TUPLE

TARGET_LIST = []

# Input file
with open(BASE_URL + FILE_NAME, 'r') as file:
    for line in file:
        # Split up from line to attribute and append to TARGET_LIST
        member = line[:-2].split(' ')
        member = list(filter(None, member))
        member = [float(attribute) for attribute in member]
        TARGET_LIST.append(
            (member[INPUT_INDEX], member[TARGET_INDEX]))
if TARGET_LIST.__len__() != NUM_OF_TUPLE:
    raise Exception(
        'Number of tuple in target list isn\'t correct to ', NUM_OF_TUPLE)

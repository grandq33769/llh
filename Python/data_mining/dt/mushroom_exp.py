'''
Decision tree experiment(Data minig project 2) using mushroom dataset
Date: 2017/12/1
'''
'''
Golden Rules:
1. Warts or scales on the cap.(cap-surface:fibrous&scaly)
2. A parasol or umbrella shaped cap.(cap-shaped:convex)
3. The presence of a bulbous cup or sac around the base.(stalk-root:bulbous&cup)
4. A white spore print.(spore-print-color:white)
5. The presence of a ring around the stem.(ring-number:one&two)
6. Gills that are thin and white.(gill-size:narrow;gill-color:white)
'''
'''
Data Attribute:
['class' 'cap-shape' 'cap-surface' 'cap-color' 'bruises' 'odor'
 'gill-attachment' 'gill-spacing' 'gill-size' 'gill-color' 'stalk-shape'
 'stalk-root' 'stalk-surface-above-ring' 'stalk-surface-below-ring'
 'stalk-color-above-ring' 'stalk-color-below-ring' 'veil-type' 'veil-color'
 'ring-number' 'ring-type' 'spore-print-color' 'population' 'habitat']
'''
import pandas as pd
import sys

PATH = '~/Documents/Data/mushrooms.csv'


def open_mushroom(prop):
    '''
    Args:
            prop(float): Training data proportion in range (0,1]
            num_a(int): Number of attributes used to return
    Returns:
            tr_x(Dataframe): Training input data dictionery
                        tr_y(list): Training target output
                        te_x(Dataframe): Testing input data dictionery
            te_y(list): Testing target output
    '''
    mdf = pd.read_csv(PATH, header=0)
    train_index = int(len(mdf.index) * prop) - 1
    # print(mdf.columns.values)

    train = mdf.iloc[:train_index]
    tr_x = train.iloc[:, 1:]
    tr_y = train['class'].values.tolist()

    test = mdf.iloc[train_index + 1:]
    te_x = test.iloc[:, 1:]
    te_y = test['class'].tolist()

    return tr_x, tr_y, te_x, te_y


def golden_classify(mushroom):
    '''
    Args:
            mushroom(Dataframe): A mushroom tuple
    Returns:
            type(char): e for edible, p for poisonious
    '''
    if mushroom['cap-surface'] == 'f' or mushroom['cap-surface'] == 'y':
        return 'p: Rule 1'
    elif mushroom['cap-shape'] == 'x':
        return 'p: Rule 2'
    elif mushroom['stalk-root'] == 'b' or mushroom['stalk-root'] == 'u':
        return 'p: Rule 3'
    elif mushroom['spore-print-color'] == 'w':
        return 'p: Rule 4'
    elif mushroom['ring-number'] == 'o' or mushroom['ring-number'] == 't':
        return 'p: Rule 5'
    elif mmushroom['gill-size'] == 'n' or ushroom['gill-color'] == 'w':
        return 'p: Rule 6'
    else:
        return 'e'


if __name__ == '__main__':
    TR_X, TR_Y, TE_X, TE_Y = open_mushroom(0.7)
    for inx, tup in TR_X.iterrows():
        print(tup)
        y = golden_classify(tup)
        print(y)

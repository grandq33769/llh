'''
Decision tree experiment(Data minig project 2) using mushroom dataset
Date: 2017/12/1
'''
import pandas as pd

PATH = '~/Documents/Data/mushrooms.csv'


def open_mushroom(prop, num_a=0):
    '''
    Args:
            prop(float): Training data proportion in range (0,1]
            num_a(int): Number of attributes used to return
    Returns:
            train(list): Training data list
            test(list): Testing data list
    '''
    mdf = pd.read_csv(PATH, header=0)
    train_index = int(len(mdf.index) * prop) - 1
    # print(mdf.columns.values)

    train = mdf.iloc[:train_index]
    tr_x = train.iloc[:, num_a+1:].values.tolist()
    tr_y = train['class'].values.tolist()

    test = mdf.iloc[train_index + 1:]
    te_x = test.iloc[:, num_a+1:].values.tolist()
    te_y = test['class'].tolist()

    return tr_x, tr_y, te_x, te_y


if __name__ == '__main__':
    TR_X, TR_Y, TE_X, TE_Y = open_mushroom(0.7)
    for tup in TR_X:
        print(tup)

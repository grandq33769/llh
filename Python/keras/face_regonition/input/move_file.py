'''
Created on 2017年5月17日

@author: LokHim
'''
import os
import random
import shutil
import multiprocessing as mp
from llh.Python.keras.face_regonition.input import URLBASE

BATCH_SIZE = 200
NUM_PROCESS = 5
TRAINING_PROP = 0.7
INPUT_DATA_PATH = '/Input_Data'


def seperate_data(mode, t_prop=TRAINING_PROP):
    SRC = URLBASE + INPUT_DATA_PATH + '/' + mode + '/'
    DST_TRANING = URLBASE + '/Training/' + mode + '/'
    DST_TESTING = URLBASE + '/Testing/' + mode + '/'
    '''
    num_of_file = len(
        [name for name in os.listdir(SRC) if os.path.isfile(SRC + name)])
    num_of_training = int(num_of_file * t_prop)
    num_of_testing = num_of_file - num_of_training
    dir_list = [DST_TRANING, DST_TESTING]
    num_list = [num_of_training, num_of_testing]
    print(mode + ' Training:',num_list[0],'Testing:',num_list[1])
    '''

    # for x, y in enumerate(dir_list):
    for _ in range(BATCH_SIZE):
        file = random.choice(os.listdir(SRC))
        file_str = (str(file))
        print(file_str)
        shutil.move(SRC + file_str, DST_TESTING)


if __name__ == '__main__':
    CTX = mp.get_context('spawn')  # 'spawn' for window
    pp_list = [CTX.Process(target=seperate_data, args=('Positive',))
               for _ in range(NUM_PROCESS)]
    np_list = [CTX.Process(target=seperate_data, args=('Negative',))
               for _ in range(NUM_PROCESS)]
    for p, n in zip(pp_list, np_list):
        p.start()
        n.start()

    for p, n in zip(pp_list, np_list):
        p.join()
        n.join()

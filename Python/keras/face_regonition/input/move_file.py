'''
Created on 2017年5月17日

@author: LokHim
'''
import os
import random
import shutil
import multiprocessing as mp
from llh.Python.keras.face_regonition.input import URLBASE


TRAIN_PROP = 0.7
NUM_PROCESS = 5
INPUT_DATA_PATH = '/Input_Data'

#mode: Positive/Negative #net: '12-net','12-net-calibration','24-net','24-net-calibration','48-net','48-net-calibration' #corpus : 'Training','Testing'
def seperate_data(corpus,net,mode,size,lock):
    src = URLBASE + INPUT_DATA_PATH + '/' + net + '/'+ '/' + mode + '/'
    dst_tr = URLBASE + '/' + 'Training' + '/' + '/' + net + '/' + mode + '/'
    dst_te = URLBASE + '/' + 'Testing' + '/' + '/' + net + '/' + mode + '/'

    with size.get_lock():
        if(size[0] == 0):
            size[0] = len([name for name in os.listdir(src) if os.path.isfile(os.path.join(src, name))])
            size[1] = len([name for name in os.listdir(dst_tr) if os.path.isfile(os.path.join(dst_tr, name))])
            size[2] = len([name for name in os.listdir(dst_te) if os.path.isfile(os.path.join(dst_te, name))])

    total = sum(size)
    batch_size = int((total * TRAIN_PROP)-size[1])
    dst = dst_tr
    if corpus == 'Testing':
        batch_size = int(total-batch_size-size[1]-size[2])
        dst = dst_te
        
    for size in range(int(batch_size/NUM_PROCESS)):
        flag = True
        while flag:
            try:
                file = random.choice(os.listdir(src))
            except (IndexError,ValueError):
                return
            
            file_str = str(file)
            
            try:
                shutil.move(src + file_str,  dst)
                flag = False
            except (shutil.Error,FileNotFoundError):
                continue
            
        lock.acquire()
        try:
            print('\n',net,corpus,mode,' File Moved in :')
            print(file_str)
            print('Process id:', os.getpid(),'File Remain:',int((batch_size/NUM_PROCESS) - size))
        finally:
            lock.release()

if __name__ == '__main__':
    psize = mp.Array('i',range(3))
    nsize = mp.Array('i',range(3))
    lock = mp.Lock()
    CTX = mp.get_context('spawn')  # 'spawn' for window
    tr_plist = [CTX.Process(target=seperate_data, args=('Training','12-net','Positive',psize,lock))
               for _ in range(NUM_PROCESS)]
    tr_nlist = [CTX.Process(target=seperate_data, args=('Training','12-net','Negative',nsize,lock))
               for _ in range(NUM_PROCESS)]
    te_plist = [CTX.Process(target=seperate_data, args=('Testing','12-net','Positive',psize,lock))
               for _ in range(NUM_PROCESS)]
    te_nlist = [CTX.Process(target=seperate_data, args=('Testing','12-net','Negative',nsize,lock))
               for _ in range(NUM_PROCESS)]

    total_list = [tr_plist,tr_nlist,te_plist,te_nlist]
    for plist in total_list:
        for process in plist:
            process.start()
            
    for plist in total_list:
        for process in plist:
            process.join()

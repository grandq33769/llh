'''
Date:2017/09/09
Craw Ptt article program
'''

import multiprocessing as mp
from PttWebCrawler.crawler import PttWebCrawler

NUM_OF_PROCESS = 16
START = 1
END = 25000
TITLE = 'Gossiping'


def craw(start, end, title):
    '''
    Call PttWebCrawler for Crawing
    Input: (int,int,str)
    Output: .json
    '''
    pwc = PttWebCrawler(as_lib=True)
    pwc.parse_articles(start, end, title)


if __name__ == '__main__':
    ONE = int((END - START) / NUM_OF_PROCESS)
    BEGIN = START
    CTX = mp.get_context('fork')
    PLIST = []
    for _ in range(NUM_OF_PROCESS - 1):
        finish = BEGIN + ONE
        PLIST.append(CTX.Process(target=craw, args=(BEGIN, finish, TITLE,)))
        BEGIN = finish
    PLIST.append(CTX.Process(target=craw, args=(BEGIN, END, TITLE,)))
    for p in PLIST:
        p.start()
    for p in PLIST:
        p.join()

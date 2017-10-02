'''
Date : 2017/09/16
Program for extracting PTT content to txt
'''
import os
import json
import re
from llh.Python.word_embedding import PTT_DATA_PATH


def filter_chinese(sentense):
    '''
    Filter out all non-chinese character and return a string
    Input:str
    Output:str
    '''
    try:
        return ''.join(re.findall('[\u4e00-\u9fff]+', sentense))
    except TypeError:
        return ''


def process_article(json_file):
    '''
    Convert and filter out content of article to a list
    Input: file(.json)
    Output: list()
    '''
    datas = json.load(json_file)
    rlist = list()

    for article in datas['articles']:
        try:
            rlist.append(filter_chinese(article['article_title']))
            rlist.append(filter_chinese(article['content']))
            for message in article['messages']:
                rlist.append(filter_chinese(message['push_content']))
        except KeyError:
            pass
    return rlist


if __name__ == '__main__':

    FLIST = [os.path.join(PTT_DATA_PATH, file)
             for file in os.listdir(PTT_DATA_PATH)]
    # Run all file for disable comment line
    RESULTS = list()
    for path in FLIST:
        print(path)
        with open(path, 'r') as file:
            result = list(filter(None, process_article(file)))
            RESULTS.extend(result)

    # Join wiki txt together
    with open('wiki_zh_tw.txt', 'a') as file:
        for line in RESULTS:
            file.write(line + '\n')

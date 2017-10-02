'''
Date : 2017/09/16
Program for extracting PTT content to txt
'''
import os
import json
import re
from llh.Python.word_embedding import PTT_DATA_PATH


def proc_chinese(article, combine=False):
    '''
    Filter out all non-chinese character and split or combine all chinese sentence in article
    Input:str
    Output:list
    '''
    r_list = list()
    try:
        if not combine:
            # All sentence will split and append to list
            r_list = re.findall('[\u4e00-\u9fff]+', article)
        else:
            # All sentence will combine in one sentence and append to list
            r_list.append(''.join(re.findall('[\u4e00-\u9fff]+', article)))
        return r_list
    except TypeError:
        return r_list


def process_article(json_file, split=True):
    '''
    Convert and filter out content of article to a list
    Input: file(.json), Split all sentence or combine in one article
    Output: list()
    '''
    datas = json.load(json_file)
    rlist = list()

    for article in datas['articles']:
        try:
            rlist.extend(proc_chinese(article['article_title'], not split))
            rlist.extend(proc_chinese(article['content'], not split))
            for message in article['messages']:
                rlist.extend(proc_chinese(message['push_content'], not split))
        except KeyError:
            pass
    return list(filter(None, rlist))


if __name__ == '__main__':

    FLIST = [os.path.join(PTT_DATA_PATH, file)
             for file in os.listdir(PTT_DATA_PATH)]
    # Run all file for disable comment line
    RESULTS = list()
    for path in FLIST:
        print(path)
        with open(path, 'r') as file:
            result = process_article(file)
            RESULTS.extend(result)

    # Join wiki txt together
    with open('wiki_zh_tw.txt', 'a') as file:
        for line in RESULTS:
            file.write(line + '\n')

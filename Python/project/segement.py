'''
Cut the answer into word
'''
import jieba
from llh.Python.project.input_data import word
DICT_PATH = 'D://Code/llh/Python/project/jieba_dict/'
EXAMPLE = '88'


def segement():
    '''
    Cut answer into word
    Return: Dict{sid: ans_dict}
    '''
    sdict = word()
    # jieba custom setting.
    jieba.set_dictionary(DICT_PATH + '/dict.txt.big')

    # load stopwords set
    stops = set()
    with open(DICT_PATH + '/stopwords.txt', 'r', encoding='utf-8') as swords:
        for line in swords:
            stops.add(line.strip('\n'))

    print('Before:', sdict[EXAMPLE])

    for _, ans_dict in sdict.items():
        for qno, ans in ans_dict.items():
            words = jieba.cut(ans, cut_all=False)
            clist = [
                word for word in words if word not in stops and word != ' ']
            ans_dict.update({qno: clist})

    print('After:', sdict[EXAMPLE])
    return sdict


if __name__ == '__main__':
    segement()

'''Cut the answer into word'''
import jieba
from llh.Python.project.input_data import SDICT
DICT_PATH = 'D://Code/llh/Python/project/jieba_dict/'
EXAMPLE = '116'

# jieba custom setting.
jieba.set_dictionary(DICT_PATH + '/dict.txt.big')

# load stopwords set
STOPWORDSET = set()
with open(DICT_PATH + '/stopwords.txt', 'r', encoding='utf-8') as sw:
    for line in sw:
        STOPWORDSET.add(line.strip('\n'))

#print('Before:', SDICT[EXAMPLE])

for sid, ans_dict in SDICT.items():
    for qno, ans in ans_dict.items():
        words = jieba.cut(ans, cut_all=False)
        clist = [word for word in words if word not in STOPWORDSET and word != ' ']
        ans_dict.update({qno: clist})

#print('After:', SDICT[EXAMPLE])

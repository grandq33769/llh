'''Convert all word to word2vec Vector'''

from gensim import models
from llh.Python.project.segement import SDICT

MPATH = "D:/Code/llh/Python/word_embedding/"
MODEL = models.Word2Vec.load(MPATH + 'med250.model.bin')
NULL_SET = set()

for sid, ans_dict in SDICT.items():
    for qno, ans_list in ans_dict.items():
        word_dict = dict()
        for word in ans_list:
            try:
                # Representation as Vector
                '''
                vector = MODEL.wv[word]
                word_dict.update({word: vector})
                '''
                # Representation as Similarity of Top5
                slist = MODEL.most_similar(word, topn=5)
                word_dict.update({word: [v[0] for v in slist]})

            except KeyError:
                print(sid, word)
                NULL_SET.add(word)
                word_dict.update({word: 0})

        ans_dict.update({qno: word_dict})
        print(sid, qno, " Update Finish")

'''
Date:2017/08/22
Clustering of all words
'''
import csv
import pickle
import numpy as np
from sklearn.cluster import KMeans
from gensim import models
from llh.Python.project import DPATH

MPATH = "D:/Code/llh/Python/word_embedding/"
MODEL = models.Word2Vec.load(MPATH + 'med250.model.bin')
FILE_PATH = DPATH + '/結果/csv/校園友善問卷資料_文字_結果(Sim).csv'


def main():
    '''Main process for K-Means of word2vec'''
    corpus = set()

    print('Input words to set(). Begin...', end='')
    with open(FILE_PATH, 'r', encoding='utf-8') as csvfile:
        raw = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in raw:
            # print(row[2:8])
            slist = list(filter(None, row[2:8]))
            corpus.update(slist)
    print('Finish!')

    print('Convert words to vector. Begin...', end='')
    corpus = list(corpus)
    wlist = list()
    vlist = list()
    null = list()

    for word in corpus:
        try:
            vector = MODEL.wv[word]
            wlist.append(word)
            vlist.append(vector)
        except KeyError:
            null.append(word)
    print('Finish!')

    print('K-Means Clustering. Begin...')
    trainig = np.array(vlist)
    all_result = dict()

    for cluster in range(10, 41):
        print(cluster, 'Clustering Training Begin...', end='')
        result = KMeans(n_clusters=cluster, random_state=0).fit(trainig)
        all_result.update({cluster: result})
        print('Finish!')
    print('K-Means Clustering. Finish!')

    print('Save Result Begin...', end='')
    with open('word_result.pickle', 'wb') as file:
        pickle.dump([wlist, all_result], file)
    print('Finish!')


if __name__ == '__main__':
    main()

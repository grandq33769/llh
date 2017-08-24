'''
Date:2017/08/22
Clustering of all words
'''
import pickle
import numpy as np
from sklearn.cluster import KMeans
from gensim import models
from llh.Python.project import CPATH, MPATH
from llh.Python.project.input_data import word_sim


def cluster(num_cluster):
    '''Main process for K-Means of word2vec'''
    corpus = set()
    model = models.Word2Vec.load(MPATH + '/med250.model.bin')

    print('Input words to set(). Begin...', end='')
    wdict = word_sim()
    for _, wset in wdict.items():
        corpus.update(wset)
    print('Finish!')

    print('Convert words to vector. Begin...', end='')
    corpus = list(corpus)
    wlist = list()
    vlist = list()
    null = list()

    for word in corpus:
        try:
            vector = model.wv[word]
            wlist.append(word)
            vlist.append(vector)
        except KeyError:
            null.append(word)
    print('Finish!')

    print(num_cluster, 'Clustering Training Begin...', end='')
    trainig = np.array(vlist)
    result = KMeans(n_clusters=num_cluster, random_state=0).fit(trainig)
    print('Finish!')

    print('Save Result Begin...', end='')
    with open(CPATH + '/cluster/word_cluster(' + str(num_cluster) + ').pickle', 'wb') as file:
        pickle.dump([wlist, result], file)
    print('Finish!')


if __name__ == '__main__':
    cluster(10)

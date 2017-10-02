'''
Module for processing word2vec
Date:2017/9/30
'''
import logging as log
from jieba import cut
from gensim import models


class Word2vecConverter():
    '''
    Class for process word2vec by given word2vec model
    '''

    def __init__(self, model_p):
        log.info('Start import Word2Vec model %s...',
                 model_p.split('/')[-1])
        self.w2v = models.Word2Vec.load(model_p).wv
        self.vocab = list(self.w2v.vocab.keys())
        log.info('Success import Word2Vec model %s...',
                 model_p.split('/')[-1])

    def sen_word2vec(self, sentence):
        '''
        Input a string sentense ,then cut and convert to word2vec
        Return a list of sliced sentense and corresponding word2vec
        '''
        cut_s = list()
        r_list = list()
        for word in cut(sentence):
            cut_s.append(word)
            try:
                r_list.append(self.word2vec(word))
            except KeyError:
                log.warning('Missing word \'%s\' is dicovered...', word)
                r_list.append(None)
        return cut_s, r_list

    def sen_indexof(self, cut_sentence):
        '''
        Input a sliced sentence and
        Return list of index of the word in vocab list
        '''
        r_list = list()
        for word in cut_sentence:
            r_list.append(self.indexof(word))
        return r_list

    def indexof(self, word):
        '''
        Return an index of word in vocab list
        '''
        return self.vocab.index(word)

    def word2vec(self, word):
        '''
        Input a word and return a vector
        '''
        return self.w2v[word]


if __name__ == '__main__':
    log.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s', level=log.INFO)
    CONVERTER = Word2vecConverter(
        '/Users/lhleung/Documents/Data/Word2vec/400_include_stopword/med400.model.bin')
    CUT, VEC = CONVERTER.sen_word2vec('我是男生')
    print(CUT)
    print(CONVERTER.sen_indexof(CUT))

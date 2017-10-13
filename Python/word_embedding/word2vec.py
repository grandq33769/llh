'''
Module for processing word2vec
Date:2017/9/30
'''
import logging as log
import numpy as np
from jieba import cut
from gensim import models


class Word2vecConverter():
    '''
    Class for process word2vec by given word2vec model
    '''

    def __init__(self, model_p):
        log.info('Start import Word2Vec model %s...',
                 model_p.split('/')[-1])
        model = models.Word2Vec.load(model_p)
        self.w2v = model.wv
        self.vector_size = model.vector_size
        self.vocab = list(self.w2v.vocab.keys())
        self.vocab_len = len(self.vocab)
        log.info('Success import Word2Vec model %s...',
                 model_p.split('/')[-1])

    def sen2vec(self, sentence):
        '''
        Args:
                sentence(string): Sentence which need to be converted
        Returns:
                cut_sentence(list): sliced sentence list
                vec(np.array): Array of word2vec which concatense from each word
        '''
        cut_sentence = list(cut(sentence))
        vec = np.expand_dims(self.word2vec(cut_sentence[0]), axis=0)
        try:
            for word in cut_sentence[1:]:
                word_vec = np.expand_dims(self.word2vec(word), axis=0)
                vec = np.concatenate((vec, word_vec))
        except IndexError:
            return cut_sentence, vec
        return cut_sentence, vec

    def sen_indexof(self, cut_sentence):
        '''
        Args:
                cut_sentence(list): List of sliced sentence string
        Returns:
                (np.array): Array of index of the word in vocab list
        '''
        r_list = list()
        for word in cut_sentence:
            r_list.append(self.indexof(word))
        # Reminder: Depends on target format, it can be list only
        return r_list

    def sen_index_vec(self, cut_sentence):
        '''
        Args:
                cut_sentence(list): List of sliced sentence string
        Returns:
                (np.array):Array of 1-n bag of words
        '''
        r_arr = np.zeros(self.vocab_len)
        index = self.indexof(cut_sentence[0])
        if index is not -1:
            r_arr[index] = 1
        r_arr = np.expand_dims(r_arr, axis=0)
        for word in cut_sentence[1:]:
            temp = np.zeros(self.vocab_len)
            index = self.indexof(word)
            if index is not -1:
                temp[index] = 1

            r_arr = np.concatenate((r_arr, np.expand_dims(temp, axis=0)))

        return r_arr

    def indexof(self, word):
        '''
        Args:
                word(string): Chinese word or vocab
        Returns:
                index(int): An index of word in vocab list
                If the word is not in w2v, -1 will be returned.
        '''
        try:
            index = self.vocab.index(word)
        except ValueError:
            index = -1
        return index

    def word2vec(self, word):
        '''
        Args:
                word(string): Chinese word or vocab
        Returns:
                (np.array): Array of vector corresponding to word
                If word doesn't exist in dict, array full of zeros will be returned
        '''
        try:
            return self.w2v[word]
        except KeyError:
            log.warning('Missing word \'%s\' is dicovered...', word)
            return np.zeros(self.vector_size)


if __name__ == '__main__':
    log.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s', level=log.INFO)
    CONVERTER = Word2vecConverter(
        '/Users/lhleung/Documents/Data/Word2vec/400_include_stopword/med400.model.bin')
    CUT, VEC = CONVERTER.sen2vec('我是男生')
    print(CUT)
    print(CONVERTER.sen_indexof(CUT))
    print(CONVERTER.vector_size)

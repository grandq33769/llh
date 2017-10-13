'''
Module for testing data processing from reading .json
Date : 2017/10/02
'''
import unittest
import logging as log
import torch.utils.data as data
import llh.Python.pytorch.ptt as ptt
from llh.Python.word_embedding.word2vec import Word2vecConverter


class TestDataProcessing(unittest.TestCase):
    '''
    Class for testing data processing
    '''

    def setUp(self):
        self.json = open(
            '/Users/lhleung/Documents/Data/Ptt/Gossiping/raw/test/Gossiping-23431-25000.json', 'r')
        self.converter = Word2vecConverter(
            '/Users/lhleung/Documents/Data/Word2vec/400_include_stopword/med400.model.bin')
        self.test_data = ptt.PTT(
            '/Users/lhleung/Documents/Data/Ptt/Gossiping/',
            False,
            False,
            self.converter.sen2vec
        )

    def tearDown(self):
        self.json.close()

    def test_read(self):
        '''
        Test case for reading .json and convert to Pytorch Dataset
        '''
        self.assertTrue(issubclass(type(self.test_data), data.Dataset))
        for index in range(1000):
            sentence, target = self.test_data.__getitem__(index)
            print(sentence)


if __name__ == '__main__':
    log.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s', level=log.INFO)
    unittest.main()

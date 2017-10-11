'''
Module for testing data processing from reading .json
Date : 2017/10/02
'''
import unittest
import logging as log
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

    def tearDown(self):
        self.json.close()

    def test_read(self):
        '''
        Test case for reading .json and extract the content
        '''
        sen, emb, labels = ptt.read_json_file(self.json, self.converter)
        self.assertEqual(len(sen), emb.size(0))
        self.assertEqual(emb.size(0), len(labels))


if __name__ == '__main__':
    log.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s', level=log.INFO)
    unittest.main()

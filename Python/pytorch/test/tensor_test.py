'''
Testing Module for testing pytorch tensor
Date : 2017/10/2
'''
import unittest
import torch


class TestTensor(unittest.TestCase):
    '''Simple test case for pytorch Tensor'''

    def setUp(self):
        self.f_tensor = torch.FloatTensor([[1, 2, 3], [4, 5, 6]])
        self.i_tensor = torch.IntTensor([[0, 0, 0], [0, 0, 0]])

    def test_type(self):
        '''Test for the type of Tensors'''
        self.assertIsInstance(self.f_tensor, torch.FloatTensor)

        i_tensor2 = torch.IntTensor(2, 3).zero_()
        self.assertTrue(self.i_tensor.equal(i_tensor2))

    def test_calculation(self):
        '''Test for tensor calculation'''
        self.assertEqual(self.f_tensor.size(), torch.Size([2, 3]))
        # repeat to desired 'times'
        self.assertEqual(
            self.f_tensor.repeat(3, 2, 3).size(), torch.FloatTensor(3, 4, 9).size())
        # expand to desired dimension
        self.assertEqual(
            self.f_tensor.expand(3, 2, 3).size(), torch.FloatTensor(3, 2, 3).size())

    @unittest.skip('Time expensive.')
    def test_input(self):
        '''Test for import word2vec to tensor'''
        from llh.Python.word_embedding.word2vec import Word2vecConverter
        converter = Word2vecConverter(
            '/Users/lhleung/Documents/Data/Word2vec/400_include_stopword/med400.model.bin')
        cut_s, s_vec = converter.sen_word2vec('我是男生')
        self.assertIsInstance(s_vec, list)
        self.assertEqual(len(s_vec), 3)
        s_tensor = torch.FloatTensor(s_vec)
        self.assertEqual(s_tensor.size(), torch.Size([len(cut_s), 400]))
        print(s_tensor.expand(1, len(cut_s), 400))

    def test_operation(self):
        '''
        Test tensor concatenate or some tensor operation
        '''
        exp_tensor = self.f_tensor.expand(1, 2, 3)
        print(exp_tensor)
        tensor2 = torch.FloatTensor(1, 3, 4).zero_()
        print(tensor2)
        cat_tensor = torch.cat((exp_tensor, exp_tensor), 0)
        self.assertEqual(cat_tensor.size(), torch.Size([2, 2, 3]))
        print(cat_tensor[0])


if __name__ == '__main__':
    unittest.main()

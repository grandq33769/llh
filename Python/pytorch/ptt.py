'''
Module to load PTT data to pytorch form for torch.dataloader
Date : 2017/9/30
'''
import os
import logging as log
import errno
import torch
import torch.utils.data as data
from llh.Python.word_embedding.extract import process_article


class PTT(data.Dataset):
    '''
    A class used to process PTT json data for pytorch data loader

    Args:
        root (string): Root directory of dataset where ``processed/training.pt``
            and  ``processed/test.pt`` exist.
        train (bool, optional): If True, creates dataset from ``training.pt``,
            otherwise from ``test.pt``.
        transform (callable, optional): A function/transform that  takes in an json file
            and returns a transformed version. E.g, ``transforms.RandomCrop``
    '''
    RAW_F = 'raw'
    PROCESSED_F = 'processed'
    TRAIN = 'training.pt'
    TEST = 'test.pt'

    def __init__(self, root, train=True,
                 processed=False, transform=None, target_transform=None):
        self.root = os.path.expanduser(root)
        self.train = train  # training set or test set
        self.processed = processed
        self.transform = transform
        self.target_transform = target_transform
        if self.train:
            self.raw_path = os.path.join(self.root, self.RAW_F, 'train')
        else:
            self.raw_path = os.path.join(self.root, self.RAW_F, 'test')
        self.proc_path = os.path.join(self.root, self.PROCESSED_F)

        if processed is False:
            self._process()

        if not self._check_exists():
            raise RuntimeError('Dataset not found,' +
                               ' Please correct the path or Switch the processed parameter.')

        if self.train:
            self.train_data = torch.load(
                os.path.join(self.proc_path, self.TRAIN))
        else:
            self.test_data = torch.load(
                os.path.join(self.proc_path, self.TEST))

    def __getitem__(self, index):
        """
        Args:
            index (int): Index
        Returns:
            sentence(list): A list of word from sliced sentence or whole sentence
            emb(np.array): Array of word2vec which concatense
                           from each word correspoding to sentence
            target(list/np.array/string):  Index list of word from sliced sentence/
                                           Array of each word(1-n bag of words)/
                                           Whole sentence
        """
        if self.train:
            sentence = self.train_data[index]
        else:
            sentence = self.test_data[index]

        if self.transform is not None:
            sentence, emb = self.transform(sentence)

        if self.target_transform is not None:
            target = torch.FloatTensor(self.target_transform(sentence))
        else:
            target = torch.FloatTensor(emb)

        return sentence, target

    def __len__(self):
        if self.train:
            result = len(self.train_data)
        else:
            result = len(self.test_data)
        return result

    def _check_exists(self):
        if self.train:
            result = os.path.exists(os.path.join(
                self.proc_path, self.TRAIN))
        else:
            result = os.path.exists(os.path.join(
                self.proc_path, self.TEST))

        return result

    def _check_raw(self):
        '''
        Check the ptt .json file is in the raw path
        '''
        return any([file.endswith('.json') for file in os.listdir(self.raw_path)])

    def _process(self):
        '''
        The function to convert PTT data in type of .json to .pt
        '''
        if self._check_exists():
            log.info('Pytorch file already exist. Please switch off processed arg')
            return

        log.info('Processing...')
        try:
            if not self._check_raw():
                raise FileNotFoundError(
                    'Raw PTT .json file is not exist in root. Please check out.')
            os.makedirs(os.path.join(self.proc_path))
        except OSError as err:
            if err.errno == errno.EEXIST:
                pass
            else:
                raise

        save_data = list()

        for json_n in (file for file in os.listdir(self.raw_path) if file.endswith('.json')):
            with open(os.path.join(self.raw_path, json_n), 'r') as json:
                log.info('Processing %s ...', json_n)
                sentences = process_article(json)
                save_data.extend(sentences)

        log.info('Saving ...')
        if self.train:
            with open(os.path.join(self.proc_path, self.TRAIN), 'wb') as file:
                torch.save(save_data, file)
        else:
            with open(os.path.join(self.proc_path, self.TEST), 'wb') as file:
                torch.save(save_data, file)
        log.info('Done !')

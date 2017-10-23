'''
Module for implementation of apriori algorithm
Date: 2017/10/23
'''
from abc import ABC, abstractmethod


class Model(ABC):
    '''
    Abstract class model for Apriori Model
    Abstract method should be implemented
    '''
    @abstractmethod
    def __init__(self, data, min_sup):
        '''
        Args:
            data(list(list)): List containing transaction in form of another list
            min_sup(float): Minimum support for apriori [0,1]
        '''
        self.data = data
        self.min_sup = min_sup
        self.org = self.initial()

    def run(self):
        '''
        Returns:
            fqits(list(frozenset)): List of frozen set containing the Frequent Itemset
        '''
        self.result = list()

        comb = self.org
        while not self.isfinish(comb):
            counts = self.count(comb)
            purned = self.purn(counts)
            self.result.extend(purned)
            comb = self.recombine(purned)

    @abstractmethod
    def initial(self):
        '''
        Returns:
            r_set(set): Set of containing all element in data set
        '''
        pass

    @abstractmethod
    def isfinish(self, comb):
        '''
        Args:
            comb(set): Set of combination to be determined
        Returns:
            True: finished of algorithm, combination in comb have be counted
            False: unfininsh, combination in comb have not be counted
        '''
        pass

    @abstractmethod
    def count(self, comb):
        '''
        Args:
            comb(set): Set of combination to be count in dataset
        Returns:
            r_set((frozenset,counts)): Set containing sets of Frozenset and its counts
        '''
        pass

    @abstractmethod
    def purn(self, counts):
        '''
        Args:
            counts((fronzenset,counts)): Set will be purned by self.min_sup
        Returns:
            r_set((frozenset,counts)): Set of remaining set (frozen,counts) that above min_sup
        '''
        pass

    @abstractmethod
    def recombine(self, purned):
        '''
        Args:
            purned(set(frozenset,counts)): Purned set that to be form new combination
        Retruns:
            r_set(frozenset): New combination set of frozenset to be counted next iteration
        '''
        pass

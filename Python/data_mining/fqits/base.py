'''
Module of Frequent Item Set based-model
Date: 2017/10/30
'''
import logging as log
from abc import ABC, abstractmethod


class FrequentItemSet(ABC):
    '''
    Abstract class model for Apriori Model
    TODO:Abstract method should be implemented
    '''
    @abstractmethod
    def __init__(self, data, min_sup):
        '''
        Args:
            data(tuple(tuple)): Tuple containing transaction in form of another tuple
            min_sup(float): Minimum support for apriori [0,1]

        Attribute:
            org(set): Set of containing all element in data set
            result({frozenset:int}):
            Dictionary of results each tuple containing itemset as key and count as value
        '''
        self.data = data
        self.min_sup = min_sup
        self.org = self.initial()
        self.result = dict()

    @abstractmethod
    def run(self):
        '''
        Returns:
            self.result({frozenset:int}):
            Dictionary of frozenset(key) represent Frequent Itemset and int(value) as counts
        '''
        pass

    def initial(self):
        '''
        Returns:
            r_set(set): Set of containing all element in data set
        '''
        r_set = set()
        for trans in self.data:
            r_set.update(set(trans))

        log.info('Initialization Success ... Number of elements: %d',
                 len(r_set))
        return r_set

    @abstractmethod
    def isfinish(self, comb):
        '''
        Args:
            comb({frozenset}): Set of combination to be determined
        Returns:
            True: finished of algorithm, combination in comb have be counted
            False: unfininsh, combination in comb have not be counted
        '''
        pass

    @abstractmethod
    def count(self, combs):
        '''
        Args:
            comb({frozenset}): Set of combination to be count in dataset
        Returns:
            r_dict({frozenset:int}):
            Dictionary containing combination of Frozenset as key and its counts as value
        '''
        pass

    @abstractmethod
    def purn(self, counts):
        '''
        Args:
            counts({frozenset:int}): Dictionary will be purned by self.min_sup
        Returns:
            r_dict({frozenset:int}): Dictionary of remaining dict {frozenset,int} that above min_sup
        '''
        pass

    @abstractmethod
    def recombine(self, purned):
        '''
        Args:
            purned({frozenset,counts}): Purned set that to be form new combination
        Retruns:
            r_set({frozenset}): New combination set of frozenset to be counted next iteration
        '''
        pass


def transform(items):
    '''
    Args:
        items(set): Set of each element item

    Returns:
        r_set((frozenset)): Set of frozenset of item
    '''
    return set(frozenset({element}) for element in items)

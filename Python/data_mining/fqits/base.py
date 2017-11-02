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

    def isfinish(self, comb):
        '''
        Args:
            comb({frozenset}): Set of combination to be determined
        Returns:
            True: finished of algorithm, combination in comb have be counted
            False: unfininsh, combination in comb have not be counted
        '''
        return not bool(comb)

    def count(self, combs):
        '''
        Args:
            comb({frozenset}): Set of combination to be count in dataset
        Returns:
            r_dict({frozenset:int}):
            Dictionary containing combination of Frozenset as key and its counts as value
        '''
        r_dict = dict()
        for com in combs:
            for trans in self.data:
                update_comb(r_dict, trans, com)
        log.info('Counting Finish ... Number of combination counts: %d',
                 len(r_dict))
        return r_dict

    def purn(self, counts):
        '''
        Args:
            counts({frozenset:int}): Dictionary will be purned by self.min_sup
        Returns:
            r_dict({frozenset:int}): Dictionary of remaining dict {frozenset,int} that above min_sup
        '''
        cond = len(self.data) * self.min_sup
        r_dict = {key: value for key, value in counts.items() if value > cond}
        log.info('Purning Finish ... Number of remaing combination: %d',
                 len(r_dict))
        return r_dict


def transform(items):
    '''
    Args:
        items(set): Set of each element item

    Returns:
        r_set((frozenset)): Set of frozenset of item
    '''
    return set(frozenset({element}) for element in items)


def update_comb(results, trans, itemset):
    '''
    Update the result dictionary
    by determinating the presence of itemset in transaction
    Args:
        results({frozenset:int}):
        Dictionary of results each tuple containing itemset as key and count as value
        trans(list): List of items in a transaction
        itemset(frozenset): Item set to be counted
    '''
    tset = set(trans)
    if not itemset.issubset(tset):
        return
    try:
        results[itemset] += 1
    except KeyError:
        results.update({itemset: 1})

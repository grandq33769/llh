'''
Module for implementation of apriori algorithm
Date: 2017/10/23
'''
import logging as log
from abc import ABC, abstractmethod
from itertools import combinations


class Apriori(ABC):
    '''
    Abstract class model for Apriori Model
    TODO:Abstract method should be implemented
    '''
    @abstractmethod
    def __init__(self, data, min_sup):
        '''
        Args:
            data(list(list)): List containing transaction in form of another list
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

    def run(self):
        '''
        Returns:
            self.result({frozenset:int}):
            Dictionary of frozenset(key) represent Frequent Itemset and int(value) as counts
        '''
        comb = transform(self.org)
        while not self.isfinish(comb):
            log.info('Round %d Begin ...', len(next(iter(comb))))
            counts = self.count(comb)
            purned = self.purn(counts)
            self.result.update(purned)
            comb = self.recombine(purned)

        return self.result

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
            comb({frozenset}): Set of combination to be determined
        Returns:
            True: finished of algorithm, combination in comb have be counted
            False: unfininsh, combination in comb have not be counted
        '''
        pass

    @abstractmethod
    def count(self, comb):
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


class Naive(Apriori):

    def __init__(self, data, min_sup):
        super(Naive, self).__init__(data, min_sup)

    def initial(self):
        r_set = set()
        for trans in self.data:
            r_set.update(set(trans))

        log.info('Initialization Success ... Number of elements: %d',
                 len(r_set))
        return r_set

    def isfinish(self, comb):
        return not bool(comb)

    def count(self, combs):
        r_dict = dict()
        for com in combs:
            for trans in self.data:
                update_comb(r_dict, trans, com)
        log.info('Counting Finish ... Number of combination counts: %d',
                 len(r_dict))
        return r_dict

    def purn(self, counts):
        cond = len(self.data) * self.min_sup
        r_dict = {key: value for key, value in counts.items() if value > cond}
        log.info('Purning Finish ... Number of remaing combination: %d',
                 len(r_dict))
        return r_dict

    def recombine(self, purned):
        if not purned:
            return {}
        tlen = len(next(iter(purned))) + 1
        prev = set(purned.keys())
        cset = set()

        log.info('Finish Lenght %d Round ... Recombination begin ...', tlen - 1)
        for comb in prev:
            cset.update(comb)

        r_set = set()
        for comb in combinations(cset, tlen):
            if check_comb(comb, prev):
                r_set.add(frozenset(comb))

        return r_set


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
    for item in itemset:
        if item not in tset:
            return
    try:
        results[itemset] += 1
    except KeyError:
        results.update({itemset: 1})


def transform(items):
    '''
    Args:
        items(set): Set of each element item

    Returns:
        r_set((frozenset)): Set of frozenset of item
    '''
    return set(frozenset({element}) for element in items)


def check_comb(combination, previous):
    '''
    Check combination is valid from previous itemset
    Args:
        combination(tuple): Candidate after recombination for next count
        previous(set): Set of Itemsets from previous count

    Returns:
        True: Inputted combination is valid for next count
        False: Inputted combination should be exclude from next round counting
    '''
    plen = len(combination) - 1
    for pre_comb in combinations(combination, plen):
        if set(pre_comb) not in previous:
            return False

    return True


Apriori.register(Naive)

if __name__ == '__main__':
    log.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s', level=log.INFO)
    from llh.Python.data import anime
    DATA1 = anime.open_data(anime.zscore)
    APRIORI = Naive(DATA1, 0.01)
    RESULT = APRIORI.run()
    for fqits, count in RESULT.items():
        print(fqits, count)

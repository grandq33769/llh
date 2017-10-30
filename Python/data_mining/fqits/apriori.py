'''
Module for implementation of apriori algorithm
Date: 2017/10/23
'''
import logging as log
from itertools import combinations

from llh.Python.data_mining.fqits.base import FrequentItemSet, transform


class Apriori(FrequentItemSet):
    '''
    Concrete class extends from Apriori
    which implements the navie-based apriori
    '''

    def __init__(self, data, min_sup):
        super(Apriori, self).__init__(data, min_sup)

    def run(self):
        comb = transform(self.org)
        while not self.isfinish(comb):
            log.info('Round %d Begin ...', len(next(iter(comb))))
            counts = self.count(comb)
            purned = self.purn(counts)
            self.result.update(purned)
            comb = self.recombine(purned)

        return self.result

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


FrequentItemSet.register(Apriori)

if __name__ == '__main__':
    log.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s', level=log.INFO)
    from llh.Python.data import anime
    DATA1 = anime.open_data(anime.zscore)
    APRIORI = Apriori(DATA1, 0.01)
    RESULT = APRIORI.run()
    for fqits, count in RESULT.items():
        print(fqits, count)

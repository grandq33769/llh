'''
Module for implementation of apriori algorithm
Date: 2017/10/23
'''
import logging as log
from itertools import combinations

from llh.Python.data_mining.fqits.base import FrequentItemSet, transform

NUM = 12000


class Apriori(FrequentItemSet):
    '''
    Concrete class extends from Apriori
    which implements the navie-based apriori
    '''

    def __init__(self, data, min_sup):
        super(Apriori, self).__init__(data[:NUM], min_sup)

    def run(self):
        comb = transform(self.org)
        while not self.isfinish(comb):
            log.info('Round %d Begin ...', len(next(iter(comb))))
            counts = self.count(comb)
            pruned = self.prune(counts)
            self.result.update(pruned)
            comb = self.recombine(pruned)

        return self.result

    def recombine(self, pruned):
        '''
        Args:
            pruned({frozenset,counts}): pruned set that to be form new combination
        Retruns:
            r_set({frozenset}): New combination set of frozenset to be counted next iteration
        '''
        if not pruned:
            return {}
        tlen = len(next(iter(pruned))) + 1
        prev = set(pruned.keys())
        cset = set()

        log.info('Finish Lenght %d Round ... Recombination begin ...', tlen - 1)
        for comb in prev:
            cset.update(comb)

        r_set = set()
        for comb in combinations(cset, tlen):
            if check_comb(comb, prev):
                r_set.add(frozenset(comb))

        return r_set


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
    APRIORI = Apriori(DATA1, 0.6)
    RESULT = APRIORI.run()
    for fqits, count in RESULT.items():
        print(fqits, count)

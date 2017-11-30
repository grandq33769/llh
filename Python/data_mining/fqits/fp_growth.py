'''
Module for implementation of FP Growth alogorithm
Date : 2017/10/30
'''
import sys
import logging as log
from collections import Counter

from llh.Python.data_structure.tree import Node
from llh.Python.data_mining.fqits.base import FrequentItemSet, transform

NUM = 12000


class FPgrowth(FrequentItemSet):
    '''
    Concrete class of model FrequentItemSet for implement FPgrowth
    '''

    def __init__(self, data, min_sup):
        super(FPgrowth, self).__init__(data[:NUM], min_sup)
        counts = self.count(transform(self.org))
        self.fpt = FPtree(counts)

    def run(self):
        num = 1
        for trans in self.data:
            self.fpt.add(trans)
            num += 1
            if num % 1000 == 0:
                log.info('Finish Processing %d of transactions ....', num)
        log.info('Finish Building FPTree....')

        self.grow(self.fpt)

        return self.result

    def grow(self, tree, condition=None):
        '''
        Args:
            tree(FPtree): FPtree for growing and count the pattern
            condition(set): Set of condition to grow tree
        '''
        log.info('Growing for condition %s Begin ...', str(condition))
        pruned = self.prune(tree.cand)

        if not self.isfinish(set(pruned.keys())):
            for item in sorted(tuple(pruned.keys()), key=lambda x: pruned[x]):
                new_tree, count = tree.extract(item)
                target = set(item)
                if condition:
                    target.update(condition)
                self.result.update({frozenset(target): count})
                self.grow(new_tree, target)


FrequentItemSet.register(FPgrowth)


class FPtuple(object):
    '''
    Class for the value of FPtree
    Attribute:
        item(frozenset): Item in a transaction
        count(int): Occurency of the item
    '''

    def __init__(self, item, count):
        self.item = item
        self.count = count

    def copy(self):
        '''
        Returns:
            c_tuple(FPtuple): A deep copy of self
        '''
        typ = type(self)
        return typ(self.item, self.count)

    def __str__(self):
        return '({},{})'.format(str(self.item), str(self.count))


class FPnode(Node):
    '''
    Subclass of llh.Python.data_structure.tree.Node
    Specialize for processing FPtuple()
    '''

    def equal(self, value):
        '''
        Determine whether the value can represent to node
        Args:
            value(frozenset/
            ): value of frozenset in a transaction
        Returns:
            True: If value equal to self.value(FPtuple).item
            False: value is not equal to self.value(FPtuple).item
        '''

        equal = False
        if isinstance(value, frozenset) and self.value.item == value:
            equal = True
        else:
            if isinstance(value, FPtuple) and self.value.item == value.item:
                equal = True
            elif isinstance(value, type(None)) and self.value is value:
                equal = True

        return equal

    @classmethod
    def _copy(cls, value):
        '''
        Args:
            child(bool): Is its child copy to new node
        Returns:
            new(Node): Returned node copy from calling node
        '''
        if value:
            new = value.copy()
        else:
            new = value

        return new

    def trace(self):
        '''
        Returns:
            r_node(FPnode):
                New node consist the path from self node to root node(Bottom Up) with self node count
            r_dict({item:count}):
                Dictionary of item occurrency
        '''
        if not isinstance(self.parent, FPnode):
            return None

        elif isinstance(self.parent.value, type(None)):
            return self.parent.copy(), dict()

        curr = self.parent
        s_node = self.parent.copy()
        s_node.value.count = self.value.count
        r_dict = {s_node.value.item: s_node.value.count}
        while curr.parent.value:
            top = curr.parent.copy()
            top.value.count = self.value.count
            top.add(s_node)

            curr = curr.parent
            s_node = top
            r_dict.update({s_node.value.item: s_node.value.count})

        r_node = FPnode(None)
        r_node.add(s_node)
        return r_node, r_dict

    def join(self, new):
        '''
        join() will sum up the count and join together with same path(Same item)
        Args:
            new(

            ): New incoming to join with self
        '''
        if self.equal(new.value):
            self._join(new.value)
            for chil in new.childs:
                nex = self.get(chil.value)
                if nex is None:
                    self.add(chil)
                else:
                    nex.join(chil)

        else:
            self.parent.add(new)

    def _join(self, value):
        '''
        Args:
            value(FPtuple/None):
                FPtuple: Sum up the count
                None: Nothing to do
        '''
        if isinstance(value, FPtuple):
            self.value.count += value.count


class FPtree(object):
    '''
    Class of FPtree
    Attribute:
        tree(

        ): Root node represent the whole tree
        cand({frozenset: int}):
            Candidate dictionary for all lenght 1 itemsets with count(int)
        linked({frozenset: set}):
            Dictionary refer to the itemset(key) containing linked list(set)
    Args:
        candidate({frozenset: int}):
            Candidate dictionary for all lenght 1 itemsets with count(int)
    '''

    def __init__(self, candidate, tree=None):
        self.cand = candidate
        self.linked = {item: set() for item in self.cand.keys()}

        if tree:
            self.tree = tree
            self.link(tree)

        else:
            self.tree = FPnode(None)

    def __str__(self):
        return self.tree.all()

    def sort(self, trans):
        '''
        Args:
            trans(tuple): Transaction tuple for sorting
        Returns:
            tuple: Sorted tuple by counts of self.cand in descending order
        '''
        return tuple(i for i in sorted(trans, key=lambda x: -self.cand[frozenset([x])]))

    def link(self, node):
        # TODO:Bottleneck
        '''
        Args:
            node(FPnode): Node will link with the tree responding to its value
        '''
        if isinstance(node, FPnode):
            if isinstance(node.value, FPtuple):
                self._link(node)

            for child in node.childs:
                self.link(child)

    def _link(self, node):
        '''
        Args:
            node(

            ): 
             will link with the tree responding to its value
        '''
        try:
            self.linked[node.value.item].add(node)
        except KeyError:
            raise KeyError(
                'Candidate do not contain all item in transactions.')

    def add(self, trans):
        '''
        Args:
            trans(tuple): Transaction need to be added to tree
        '''
        curr = self.tree
        for item in self.sort(trans):
            fitem = frozenset([item])
            nex = curr.get(fitem)
            if nex is None:
                value = FPtuple(fitem, 0)
                nex = FPnode(value, parent=curr)
            self.link(nex)

            nex.value.count += 1
            curr = nex

    def extract(self, item):
        '''
        Args:
            item(frozenset): Sub tree condition by this item
        Returns:
            r_tree(FPtree): New root node condition by input item
            count(int): Count of the item occurency
        '''
        if item not in self.cand.keys():
            return None, 0

        new_node = FPnode(None)
        cand = Counter()

        for node in self.linked[item]:
            trace, c_dict = node.trace()

            new_node.join(trace)
            cand += Counter(c_dict)

        # Important
        # print(item, self.cand[item], cand)

        return FPtree(dict(cand), new_node), self.cand[item]


if __name__ == '__main__':
    log.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s', level=log.INFO)
    from llh.Python.data import anime
    DATA1 = anime.open_data(anime.zscore)
    FP = FPgrowth(DATA1, 0.6)
    RESULT = FP.run()

    for fqits, count in RESULT.items():
        print(fqits, count)

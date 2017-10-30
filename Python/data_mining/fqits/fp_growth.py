'''
Module for implementation of FP-Growth alogorithm
Date : 2017/10/30
'''
import sys
import logging as log

from llh.Python.data_structure.tree import Node
from llh.Python.data_mining.fqits.base import FrequentItemSet, transform


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
            value(FPtuple): value of frozenset and count in a transaction
        Returns:
            True: If value equal to self.value(FPtuple).item
            False: value is not equal to self.value(FPtuple).item
        '''
        equal = False

        if isinstance(value, type(self.value)):
            if isinstance(value, FPtuple) and not (self.value.item - value.item):
                equal = True
            elif isinstance(value, type(None)) and self.value is value:
                equal = True

        return equal

    def trace(self):
        '''
        Returns:
            r_node(FPnode):
            New node consist the path from self-node to level-1 node(Bottom-Up) with self-node count
        '''
        if not self.parent.value:
            return None

        curr = self.parent
        r_node = self.parent.copy()
        while curr.parent.value:
            top = curr.parent.copy()
            top.value.count = self.value.count
            top.add(r_node)
            curr = curr.parent
            r_node = top

        return FPnode(None).add(r_node)

    def join(self, new):
        '''
        join() will sum up the count and join together with same path(Same item)
        Args:
            new(FPnode): New incoming to join with self
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
        tree(Node): Root node represent the whole tree
        cand({frozenset: int}):
            Candidate dictionary for all lenght 1 itemsets with count(int)
        dict({frozenset: set}):
            Dictionary refer to the itemset(key) containing linked list(set)
    Args:
        candidate({frozenset: int}):
            Candidate dictionary for all lenght 1 itemsets with count(int)
    '''

    def __init__(self, candidate):
        self.tree = FPnode(None)
        self.cand = candidate
        self.dict = {items: set() for items in candidate}

    def sort(self, trans):
        '''
        Args:
            trans(tuple): Transaction tuple for sorting
        Returns:
            tuple: Sorted tuple by counts of self.cand in descending order
        '''
        return tuple(i for i in sorted(trans, key=lambda x: -self.cand[frozenset(x)]))

    def add(self, trans):
        '''
        Args:
            trans(tuple): Transaction need to be added to tree
        '''
        curr = self.tree
        for item in self.sort(trans):
            fitem = frozenset(item)
            nex = curr.get(fitem)
            print(nex)
            if nex is None:
                value = FPtuple(fitem, 0)
                nex = FPnode(value, parent=curr)
            try:
                self.dict[fitem].add(nex)
            except KeyError:
                print('Your candidate set does not contain all item in data')
                sys.exit(0)

            nex.value.count += 1
            curr = nex

    def extract(self, item):
        '''
        Args:
            item(frozenset): Sub - tree condition by this item
        Returns:
            r_node(Node): New root node condition by input item
        '''
        r_node = FPnode(None)


if __name__ == '__main__':
    log.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s', level=log.INFO)
    z = FPnode(None)
    n = FPnode(FPtuple(frozenset('a'), 4))
    n1 = FPnode(FPtuple(frozenset('b'), 3))
    n11 = FPnode(FPtuple(frozenset('e'), 2))
    n12 = FPnode(FPtuple(frozenset('f'), 1))
    n2 = FPnode(FPtuple(frozenset('d'), 1))

    z2 = FPnode(None)
    m = FPnode(FPtuple(frozenset('a'), 4))
    m2 = FPnode(FPtuple(frozenset('d'), 4))
    m21 = FPnode(FPtuple(frozenset('c'), 4))

    z2.add(m)
    m.add(m2)
    m2.add(m21)

    n1.add(n11)
    n1.add(n12)

    n.add(n1)
    n.add(n2)

    z.add(n)

    z.join(z2)
    print(z.all())

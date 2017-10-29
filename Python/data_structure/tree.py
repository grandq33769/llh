'''
Module for impletement Tree data structure
Date : 29/10/2017
'''


class Node(object):
    '''
    Basic class for generic tree
    '''

    def __init__(self, value, parent=None, child=None):
        '''
        Simplest constructor for creating a basic tree
        Args:
            value(object): The object be contained in node
            parent(Node): Parent node for linking with self node
            child(list(Node)): Child node for being self node child
        '''
        self.level = 1
        self.value = value
        self.parent = None
        self.childs = []

        if parent is not None:
            assert isinstance(parent, Node)
            parent.add(self)
            self.parent = parent

        if child is not None:
            self.add(child)

    def add(self, child):
        '''
        Args:
            child(Node/list(Node)): Node for being added as child
                                    list of Node to being added as child
        '''
        root = self.get_root()
        assert root.exist(child) is False
        if isinstance(child, list):
            for chil in child:
                self._add(chil)
        else:
            self._add(child)

    def _add(self, child):
        '''
        Args:
            child(Node): Node to be added as child
        '''
        assert isinstance(child, Node)
        child.add_level(self.level)
        child.parent = self
        self.childs.append(child)

    def add_level(self, level):
        '''
        Add level for itself and all its child
        Args:
            level(int): level need to be added
        '''
        self.level = level + 1
        for chil in self.childs:
            chil.add_level(self.level)

    def delete(self, value):
        '''
        Args:
            value(object/Node): Object being contained in child node that which be deleted
                                Node for directly delete
        '''
        d_list = [chil for chil in self.childs if chil.value == value]
        if isinstance(value, Node):
            d_list.append(value)
        for item in d_list:
            self.childs.remove(item)

    def delete_all(self, value):
        '''
        Args:
            value(object): Object being contained in "All" child node that which be deleted
        '''
        self.delete(value)
        for chil in self.childs:
            chil.delete(value)

    def all(self):
        '''
        Returns:
            str: All node data include (Depth-first search)
        '''
        r_str = ''
        r_str += self.__str__() + '\n'
        for chil in self.childs:
            r_str += chil.all()
        return r_str

    def exist(self, node):
        '''
        Args:
            node(Node): Node to be determined whether is in the tree
        Retruns:
            True: Node is already in the tree
            False: Node have not in the tree
        '''
        if self is node:
            return True

        else:
            for child in self.childs:
                if child.exist(node):
                    return True

        return False

    def get_root(self):
        '''
        Returns:
            Node: the root of node
        '''
        if self.level is 1:
            return self

        else:
            return self.parent.get_root()

    def find(self, value):
        '''
        Args:
            Value(object): Value that desire to be found in all node (self & child)
        Returns:
            r_list(list(Node)): List of nodes contain the value
        '''
        r_list = list()
        if self.value is value:
            r_list.append(self)

        for child in self.childs:
            r_list.extend(child.find(value))

        return r_list

    def copy(self, child=False):
        '''
        Args:
            child(bool): Is its child copy to new node
        Returns:
            new(Node): Returned node copy from calling node
        '''
        new = Node(self.value)
        if child:
            for chil in self.childs:
                new.add(chil.copy(child))

        return new

    def __str__(self):
        '''
        Print all meta data of this node
        '''
        if self.parent is None:
            parent = None

        else:
            parent = self.parent.value

        return "Value: {} Level: {} Parent: {} # of Childs: {}"\
               .format(self.value, self.level, parent, len(self.childs))


if __name__ == '__main__':
    n = Node(2)
    n1 = Node('30')
    n2 = Node(3.4)
    n3 = Node(list())
    n4 = Node(3.4)

    n.add(n1)
    n1.add(n2)
    n1.add(n3)
    n3.add(n4)

    c_n2 = n2.copy()
    node = Node(3, n, c_n2)
    result = list(map(lambda x: x.level, n.find(3.4)))
    print(result)
    print(n.all())

    c_n = n1.copy(True)
    print(c_n.all())

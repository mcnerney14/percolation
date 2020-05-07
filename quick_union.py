from typing import Any
import math

class QuickUnion:
    ''' Calculates a weighted quick union to allow two
    nodes to be easily connected
    initial input: number of total elements in an array(ie 25 in 5x5 array) '''
    def __init__(self, num_elements: int):
        self.num_elements = num_elements
        self.ids = [None] * self.num_elements
        # initially initialize each node to be itself
        for i in range(num_elements):
            self.ids[i] = i
        # create a list to keep track of how many nodes each root has
        self.size = [1] * self.num_elements

    def find_root(self, id_element: int) -> int:
        while self.ids[id_element] != id_element:
            id_element = self.ids[id_element]
        return id_element

    def connected(self, id_p: int, id_q: int) -> bool:
        ''' Determines if elements are connected to each other
        by seeing if they have the same root node'''
        return self.find_root(id_p) == self.find_root(id_q)

    def union(self, id_p, id_q):
        root_p = self.find_root(id_p)
        root_q = self.find_root(id_q)
        # setting root of the smaller tree to root of the larger tree
        if self.size[id_q] < self.size[id_p]:
            self.ids[root_p] = root_q
            self.size[root_q] += self.size[root_p]
        else:  
            # print("I am here")
            self.ids[root_q] = root_p
            self.size[root_p] += self.size[root_q]

    def connection_percolates(self) -> bool:
        ''' If the root of a top node is equal to the root
        # of a bottom node, then we say the 'grid' percolates! '''
        N = int(math.sqrt(self.num_elements))
        top = set()
        bottom = set()
        for i in range(N):
            top.add(self.find_root(self.ids[i]))
            bottom.add(self.find_root(self.ids[-(i+1)]))
        for top_element in top:
            if top_element in bottom:
                return True
        return False
    
    
def test_quick_union():
    ''' A few test cases but I need some improvement here :) '''
    qu = QuickUnion(4)
    assert(qu.find_root(1) == 1)
    assert(qu.connected(0, 1) == False)
    qu.union(0, 1)
    assert(qu.ids == [0, 0, 2, 3])
    qu.union(1, 2)
    assert(qu.ids == [0, 0, 0, 3])
    print(qu.size == [2, 2, 1, 1])
    assert(qu.connected(0, 2) == True)

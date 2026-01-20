# LAB7
# REMINDER: The work in this assignment must be your own original work and must be completed alone.
# Don't forget to list any authorized forms of collaboration using a Collaboration Statement

class MaxBinaryHeap:
    '''
        >>> h = MaxBinaryHeap()
        >>> h.getMax
        >>> h.insert(10)
        >>> h.insert(5)
        >>> h
        [10, 5]
        >>> h.insert(14)
        >>> h._heap
        [14, 5, 10]
        >>> h.insert(9)
        >>> h
        [14, 9, 10, 5]
        >>> h.insert(2)
        >>> h
        [14, 9, 10, 5, 2]
        >>> h.insert(11)
        >>> h
        [14, 9, 11, 5, 2, 10]
        >>> h.insert(14)
        >>> h
        [14, 9, 14, 5, 2, 10, 11]
        >>> h.insert(20)
        >>> h
        [20, 14, 14, 9, 2, 10, 11, 5]
        >>> h.insert(20)
        >>> h
        [20, 20, 14, 14, 2, 10, 11, 5, 9]
        >>> h.getMax
        20
        >>> h._leftChild(1)
        20
        >>> h._rightChild(1)
        14
        >>> h._parent(1)
        >>> h._parent(6)
        14
        >>> h._leftChild(6)
        >>> h._rightChild(9)
        >>> h.deleteMax()
        20
        >>> h._heap
        [20, 14, 14, 9, 2, 10, 11, 5]
        >>> h.deleteMax()
        20
        >>> h
        [14, 9, 14, 5, 2, 10, 11]
        >>> len(h)
        7
        >>> h.getMax
        14
    '''

    def __init__(self):
        self._heap=[]
        
    def __str__(self):
        return f'{self._heap}'

    __repr__=__str__

    def __len__(self):
        return len(self._heap)

    @property
    def getMax(self):
        if self._heap:
            return self._heap[0]
    
    def _parent(self,heapindex):
        if (heapindex)//2 != 0:
            return self._heap[(heapindex//2)-1]
        

    def _leftChild(self,heapindex):
        if (2*heapindex)-1 < len(self._heap):
            return self._heap[(2*heapindex)-1]


    def _rightChild(self,heapindex):
        if (2*heapindex) < len(self._heap):
            return self._heap[(2*heapindex)]


    def insert(self, item):
        self._heap.append(item)
        index = len(self._heap)
        while self._parent(index) != None and index > 0 and self._parent(index) < self._heap[index-1]:
            self._heap[(index//2)-1], self._heap[index-1] = self._heap[index-1], self._heap[(index//2)-1]
            index = (index)//2

    def deleteMax(self):
        if len(self)==0:
            return None        
        elif len(self)==1:
            removed=self._heap[0]
            self._heap=[]
            return removed
        else:
            root = self._heap[0]
            self._heap[0] = self._heap.pop()
            heapindex = 1
            while 2*heapindex < len(self._heap) and self._heap[heapindex-1] < max(self._leftChild(heapindex), self._rightChild(heapindex)):
                if self._leftChild(heapindex) < self._rightChild(heapindex):
                    self._heap[2*heapindex], self._heap[heapindex-1] = self._heap[heapindex-1], self._heap[2*heapindex]
                    heapindex = 2*heapindex+1
                else:
                    self._heap[2*heapindex-1], self._heap[heapindex-1] = self._heap[heapindex-1], self._heap[2*heapindex-1]
                    heapindex = 2*heapindex
            return root
                

def heapSort(numList):
    '''
       >>> heapSort([9,1,7,4,1,2,4,8,7,0,-1,0])
       [9, 8, 7, 7, 4, 4, 2, 1, 1, 0, 0, -1]
       >>> heapSort([9,1,7,4,1,2,4,8,7,0,-1,0])
       [9, 8, 7, 7, 4, 4, 2, 1, 1, 0, 0, -1]
       >>> heapSort([-15, 1, 0, -15, -15, 8 , 4, 3.1, 2, 5])
       [8, 5, 4, 3.1, 2, 1, 0, -15, -15, -15]
    '''
    heap = MaxBinaryHeap()
    sortedList = []
    for num in numList:
        heap.insert(num)
    while len(heap) > 0:
        sortedList.append(heap.deleteMax())
    return sortedList


def run_tests():
    import doctest
    doctest.testmod(verbose=True)
    
if __name__ == "__main__":
    run_tests()
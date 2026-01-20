class MinBinaryHeap:
    def __init__(self):
        self.heapList = [0]
        self.currentSize = 0
    
    def _parent(self, index):
        return self.heapList[index // 2]

    def leftChild(self, index):
        return self.heapList[index * 2]

    def _rightChild(self, index):
        return self.heapList[index * 2 + 1]

    def getMin(self):
        return self.heapList[1]

    def insert(self, item):
        self.heapList.append(item)
        self.currentSize += 1
        self._percUp(self.currentSize)

    def _percUp(self, index):
        while index // 2 > 0:
            if self.heapList[index] < self._parent(index):
                self.heapList[index], self.heapList[index // 2] = self.heapList[index // 2], self.heapList[index]
            index = index // 2

    def deleteMin(self):
        if self.currentSize == 0:
            return None
        minVal = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize -= 1
        self.heapList.pop()
        self._percDown(1)
        return minVal

    def _percDown(self, index):
        while (index * 2) <= self.currentSize:
            minChild = self._minChild(index)
            if self.heapList[index] > self.heapList[minChild]:
                self.heapList[index], self.heapList[minChild] = self.heapList[minChild], self.heapList[index]
            index = minChild

    def _minChild(self, index):
        if (index * 2 + 1) > self.currentSize:
            return index * 2
        else:
            if self.leftChild(index) == self._rightChild(index):
                return index * 2
            else:
                if self.leftChild(index) < self._rightChild(index):
                    return index * 2
                else:
                    return index * 2 + 1

    def __len__(self):
        return self.currentSize

    def __repr__(self):
        return str(self.heapList[1:])


def heapSort(numList):
    heap = MinBinaryHeap()
    sortedList = []

    # Insert elements into heap
    for num in numList:
        heap.insert(num)

    # Remove minimum element from heap and append to sorted list until heap is empty
    while heap.len_() > 0:
        sortedList.append(heap.deleteMin())

    return sortedList



#https://www.chegg.com/homework-help/questions-and-answers/maxbinaryheap-class-8-pts-discussed-first-part-module-6-binary-heap-complete-binary-tree-s-q112683313
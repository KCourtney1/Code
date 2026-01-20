# LAB4
# REMINDER: The work in this assignment must be your own original work and must be completed alone.

class Node:   # You are not allowed to modify this class
    def __init__(self, value=None):  
        self.next = None
        self.value = value
    
    def __str__(self):
        return f"Node({self.value})"

    __repr__ = __str__

class Malloc_Library:

    """
    ** This is NOT a comprehensive test sample, test beyond this doctest
        >>> lst = Malloc_Library()
        >>> lst
        <BLANKLINE>
        >>> lst.malloc(5)
        >>> lst
        None -> None -> None -> None -> None
        >>> lst.__len__()
        5
        >>> lst[0] = 23
        >>> lst
        23 -> None -> None -> None -> None
        >>> lst[0]
        23
        >>> lst[1]
        >>> lst.realloc(7)
        >>> lst
        23 -> None -> None -> None -> None -> None -> None
        >>> lst.realloc(1)
        >>> lst
        23
        >>> lst.realloc(1)
        >>> lst
        23
        >>> lst.calloc(5)
        >>> lst
        0 -> 0 -> 0 -> 0 -> 0
        >>> lst.calloc(10)
        >>> lst[3] = 5
        >>> lst[8] = 23
        >>> lst
        0 -> 0 -> 0 -> 5 -> 0 -> 0 -> 0 -> 0 -> 23 -> 0
        >>> lst.realloc(5)
        >>> lst
        0 -> 0 -> 0 -> 5 -> 0
        >>> other_lst = Malloc_Library()
        >>> other_lst.realloc(9)
        >>> other_lst[0] = 12
        >>> other_lst[5] = 56
        >>> other_lst[8] = 6925
        >>> other_lst[10] = 78
        Traceback (most recent call last):
            ...
        IndexError


        >>> lst1=Malloc_Library()
        >>> lst2=Malloc_Library()
        >>> lst1.memcpy(5, lst2, 3, 11)
        >>> lst1.head is None
        True
        >>> lst2.head is None
        True
        >>> lst1.malloc(5)
        >>> lst1[3]= 65
        >>> lst1[0]= 72
        >>> lst1.memcpy(0, lst2, 0, 2)
        >>> lst1
        72 -> None -> None -> 65 -> None
        >>> lst2.head is None
        True
        >>> lst1.malloc(5)
        >>> lst1[3]= 65
        >>> lst1[1]= 5
        >>> lst1[0]= 1
        >>> lst1[2]= 12
        >>> lst1[4]= 33
        >>> lst1
        1 -> 5 -> 12 -> 65 -> 33
        >>> lst2.malloc(4)
        >>> lst1.memcpy(2, lst2, 1, 15)
        >>> lst2
        None -> 12 -> 65 -> 33
        >>> lst2.malloc(10)
        >>> lst2
        None -> None -> None -> None -> None -> None -> None -> None -> None -> None
        >>> lst1.memcpy(0, lst2, 0, 2)

        >>> lst
        0 -> 0 -> 0 -> 5 -> 0
        >>> other_lst
        12 -> None -> None -> None -> None -> 56 -> None -> None -> 6925
        >>> other_lst.memcpy(2, lst, 0, 5)

        >>> lst
        None -> None -> None -> 56 -> None
        >>> other_lst
        12 -> None -> None -> None -> None -> 56 -> None -> None -> 6925
        >>> temp = lst.head.next.next
        >>> lst.free()
        >>> temp.next is None
        True
    """

    def __init__(self): # You are not allowed to modify the constructor
        self.head = None
    
    def __repr__(self):  # You are not allowed to modify this method
        current = self.head
        out = []
        while current != None:
            out.append(str(current.value))
            current = current.next
        return " -> ".join(out)

    __str__ = __repr__
    
    def __len__(self):
        # --- YOUR CODE STARTS HERE
        count = 1
        current = self.head
        if self.head:
            while current.next:
                count += 1
                current = current.next
        return count

    
    def __setitem__(self, pos, value):
        # --- YOUR CODE STARTS HERE
        current = self.head
        while pos>=0 and current:
            if pos==0:
                current.value = value
            pos -= 1
            current = current.next
        if pos>0:
            raise IndexError() 


    def __getitem__(self, pos):
        # --- YOUR CODE STARTS HERE
        current = self.head
        while pos>=0:
            if pos==0:
                return current.value
            pos -= 1
            current = current.next
    

    def malloc(self, size):
        # --- YOUR CODE STARTS HERE
        self.head = Node(None)
        current = self.head
        while not size <= 1:
            current.next = Node(None)
            current = current.next
            size -= 1


    def calloc(self, size):
        # --- YOUR CODE STARTS HERE
        self.head = Node(0)
        current = self.head
        while not size <= 1:
            current.next = Node(0)
            current = current.next
            size -= 1 


    def free(self):
        # --- YOUR CODE STARTS HERE
        current = self.head
        while current:
            if current.next:
                if not current.next.next:
                    current.next = None
                    current = self.head
                current = current.next
            else:
                self.head = None
                current = self.head



    def realloc(self, size):
        # --- YOUR CODE STARTS HERE
        if not self.head:
            self.head = Node(None)
        current = self.head
        while self.__len__() != size:
            if current:
                if self.__len__()>size:
                    if size == 1:
                        current.next = None
                    elif not current.next.next:
                        current.next = None
                        current = self.head
                    current = current.next
                else:
                    if not current.next:
                        current.next = Node(None)
                    current = current.next
            else:
                self.head = Node(None)
                current = self.head

        
            





    def memcpy(self, ptr1_start_idx, pointer_2, ptr2_start_idx, size):
        # --- YOUR CODE STARTS HERE
        # copy values from original list to another list starting at specified positions and up to a given number of nodes (size)
        if self.__len__() > ptr1_start_idx and pointer_2.__len__() > ptr2_start_idx:
            if self.__len__() < size:
                self.realloc(size)
            current_ptr1 = self.head
            current_ptr2 = pointer_2.head
            ptr1_start_idx=ptr1_start_idx*-1
            ptr2_start_idx=ptr2_start_idx*-1
            while current_ptr1 and current_ptr2 and size>0:
                if ptr2_start_idx <= 0:
                    pointer_2.__setitem__(abs(ptr2_start_idx),self.__getitem__(abs(ptr1_start_idx)))
                    size -= 1
                ptr2_start_idx-=1
                ptr1_start_idx-=1
                current_ptr1 = current_ptr1.next
                current_ptr2 = current_ptr2.next


def run_tests():
    import doctest
    doctest.testmod(verbose=True)
     

if __name__ == "__main__":
     run_tests()
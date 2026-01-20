# LAB 5
# REMINDER: The work in this assignment must be your own original work and must be completed alone.

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        
    def __str__(self):
        return ("Node({})".format(self.value)) 

    __repr__ = __str__


class BinarySearchTree:
    """
        >>> my_tree = BinarySearchTree() 
        >>> my_tree.isEmpty()
        True
        >>> my_tree.isBalanced
        True
        >>> my_tree.insert(9) 
        >>> my_tree.insert(5) 
        >>> my_tree.insert(14) 
        >>> my_tree.insert(4)  
        >>> my_tree.insert(6) 
        >>> my_tree.insert(5.5) 
        >>> my_tree.insert(7)   
        >>> my_tree.insert(25) 
        >>> my_tree.insert(23) 
        >>> my_tree.getMin
        4
        >>> my_tree.getMax
        25
        >>> 67 in my_tree
        False
        >>> 5.5 in my_tree
        True
        >>> my_tree.isEmpty()
        False
        >>> my_tree.getHeight(my_tree.root)   # Height of the tree
        3
        >>> my_tree.getHeight(my_tree.root.left.right)
        1
        >>> my_tree.getHeight(my_tree.root.right)
        2
        >>> my_tree.getHeight(my_tree.root.right.right)
        1
        >>> my_tree.isBalanced
        False
        >>> my_tree.insert(10)
        >>> my_tree.isBalanced
        True
    """
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root=Node(value)
        else:
            self._insert(self.root, value)

    def _insert(self, node, value):
        if(value<node.value):
            if(node.left==None):
                node.left = Node(value)
            else:
                self._insert(node.left, value)
        else:   
            if(node.right==None):
                node.right = Node(value)
            else:
                self._insert(node.right, value)
    
    def isEmpty(self):
        # YOUR CODE STARTS HERE
        return self.root == None

    @property
    def getMin(self): 
        # YOUR CODE STARTS HERE
        min = self.root.value
        current = self.root
        while current:
            if current.value < min:
                min = current.value
            current = current.left
        return min

    @property
    def getMax(self): 
        # YOUR CODE STARTS HERE
        max = self.root.value
        current = self.root
        while current:
            if current.value > max:
                max = current.value
            current = current.right
        return max

    def __contains__helper(self, node, value):
        if node == None:    #if leaf return false(didnt find in children)
            return False
        if value == node.value:     #found value in tree
            return True
        left_side = self.__contains__helper(node.left, value)   #look for value in the left nodes
        if left_side:   #if found return value
            return left_side
        right_side = self.__contains__helper(node.right, value)     #when left side of the branch is exhusted check the right
        return right_side   #if true return else back up the tree and go down the right side of the branch until back at root.
    
    def __contains__(self,value):
        # YOUR CODE STARTS HERE
        return self.__contains__helper(self.root,value)     #needs a way to keep track of where it is in the tree, added an helper that takes a node and value to search for.
    
    def getHeight(self, node):
        # YOUR CODE STARTS HERE
        # if is a leaf will return -1
        if node == None:
            return -1
        else:
            #gets the height of the left and right branches
            left_height = self.getHeight(node.left)
            right_height = self.getHeight(node.right)
        #returns each iteration of recusion calls with +1 cumulatively minus the last brach(only counting edges)
        return max(left_height,right_height)+1


    @property
    def isBalanced(self):  # Do not modify this method
        return self.isBalanced_helper(self.root)
    
    
    def isBalanced_helper(self, node):
        # YOUR CODE STARTS HERE
        # is balanced if a node is none
        if node == None:
            return True
        left_height = self.getHeight(node.left)
        right_height = self.getHeight(node.right)
        if (-1 <= left_height-right_height<=1) and (self.isBalanced_helper(node.left)) and (self.isBalanced_helper(node.right)):    #checks current node height balance then moves on to the left when left is exhausted will then check right.
            return True     #returns true if all branches have the are balnced
        return False        #returns false if one of the braches is not -1 <= balance <= 1, then causes the and and and booleon to return fasle

def run_tests():
    import doctest
    doctest.testmod(verbose=True)
    
if __name__ == "__main__":
    run_tests()
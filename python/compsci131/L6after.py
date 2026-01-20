import math

def get_pair_sum(lst, target):
    """
        precondition: lst is an non empty list of int and target is a int
        postcondition: returns pair of number that add up to target
        Examples:
        >>> get_pair_sum([10, -1, 1, -8, 3, 1], 2)
        (10, -8)
        >>> get_pair_sum([10, -1, 1, -8, 3, 1], 2) in [ (10, -8), (-8, 10), (-1, 3), (3, -1), (1, 1) ]
        True        
        >>> get_pair_sum([10, -1, 1, -8, 3, 1], 10)
        >>> get_pair_sum([10, -1, 1, -8, 3, 1], 10) == None
        True
    """
    for num in lst:
        difference = target - num
        if difference in lst:
            return num, difference
    return None

def avg_col(lst):
    """
        precondition: which takes a 2D list of numbers as an argument
        postcondition: mutates avg to the end of the col in the list, does not return any value at all 
        Examples:
        >>> my_list =[[1, 2, 3],[4, 5, 9], [1, 8, 9]]
        >>> avg_col(my_list)       
        >>> my_list
        [[1, 2, 3], [4, 5, 9], [1, 8, 9], [2.0, 5.0, 7.0]]

        >>> my_list = [[-6, 3, 6, -3, 9], [-2, 2, -5, -6, -10], [0, -2, 3, 4, 2], [2, -9, -7, 7, -10]]
        >>> avg_col(my_list)
        >>> my_list 
        [[-6, 3, 6, -3, 9], [-2, 2, -5, -6, -10], [0, -2, 3, 4, 2], [2, -9, -7, 7, -10], [-1.5, -1.5, -0.75, 0.5, -2.25]]
    """
    row_colavg = []
    for col in range(len(lst[0])):
        avg = 0
        for row in lst:
           avg += row[col]
        row_colavg.append(avg/len(lst))
    lst.append(row_colavg)

def get_largest(lst):
    """
        precondition: takes a 2D list of numbers as an argument.
        postcondition: This function returns the largest element in lst
        Examples:
        >>> my_list =[[1, 2, 3],[4, 5, 9], [1, 8, 9]]
        >>> get_largest(my_list) 
        9
        >>> get_largest([[1, 2, 3, 4, 8], [1, 8, 9, 85, 4, 78, 45]]) 
        85
    """
    largest = lst[0][0]
    for row in lst:
        for num in row:
            if num > largest:
                largest = num
    return largest

def add_col(lst):
    """
        precondition: which takes a 2D list of numbers as an argument
        postcondition: creates a new 1D list that contains the sum for each column within the lst
        Example:
        >>> my_list =[[1, 2, 3],[4, 5, 9], [1, 8, 9]]                
        >>> add_col(my_list)     
        [6, 15, 21]
        >>> my_list                                  
        [[1, 2, 3], [4, 5, 9], [1, 8, 9]]
    """
    row_coltotal = []
    for col in range(len(lst[0])):
        total = 0
        for row in lst:
           total += row[col]
        row_coltotal.append(total)
    return row_coltotal

def is_rectangular(lst):
    """
        precondition: takes a possibly-2D (or possibly not) list lst
        postcondition: returns True if the list is a rectangular list (each row has the same number of elements), False otherwise.
        >>> is_rectangular([[1, 2, 3],[4, 5, 9], [1, 8, 9]]) 
        True
        >>> is_rectangular([[1, 2, 3, 4],[1, 8, 9, 5]])
        True
        >>> is_rectangular([1, 2, 3])
        False
        >>> is_rectangular([[1, 2, 3],4, 5, 9, [1, 8, 9]])
        False
        >>> is_rectangular([[1, 2, 3],[4, 9], [1, 8, 9]])
        False
    """
    for item in lst:
        if type(item) != list:
            return False
        if len(item) != len(lst[0]):
            return False
    return True

def has_duplicates(lst):
    """
        precondtion: takes a 2D list L of arbitrary values
        postcondition: returns True if lst contains any duplicate values, False otherwise.
        Examples:
        >>> has_duplicates([[1, 2, 3],[4, 9], [1, 8, 9]] ) 
        True
        >>> has_duplicates([[1, 2, 3, 4],[10, 8, 9, 5]])  
        False
    """
    numberscount = {}
    for row in lst:
        for num in row:
            if num in numberscount:
                numberscount[num] += 1
            else:
                numberscount[num] = 1
    for _, Value in numberscount.items():
        if Value == 2:
            return True
    return False

def most_popular(d):
    """
        precondtion: takes a dictionary with formate person:[friends]
        postcondition: returns the name that occurs the most number of times in all the lists of friends
        Examples:
        Examples:
        >>> most_popular({'ben': ['sara', 'taylor', 'phil'], 'sara': ['ben', 'taylor', 'chris']}) 
        'taylor'
        >>> most_popular({'ben': ['sara', 'taylor', 'phil'], 'sara': ['ben', 'taylor', 'chris'], 'stuart':['sara', 'phil'], 'phil':['sara', 'ben']}) 
        'sara'
    """
    name_Occurrences = {}
    for _,value in d.items():
            for name in value:
                if name in name_Occurrences:
                    name_Occurrences[name] += 1
                else:
                    name_Occurrences[name] = 1
            
    largest = -math.inf
    name = ""
    for key, value in name_Occurrences.items():
        if value > largest:
            largest = value
            name = key
    return name

def run_tests_b():
  import doctest
  doctest.run_docstring_examples(avg_col, globals(), name="HW2", verbose=True)

if __name__== "__main__":
  run_tests_b()
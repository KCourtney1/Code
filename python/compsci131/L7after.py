import math
def power(x, y):
    """
        precondition: x and y are integers greater than or equal to 0
        postconditon: returns the result of raising x to the power of y
        Examples:
        >>> power(2, 3)
        8
        >>> power(5, 1)
        5
        >>> power(655, 0)
        1
        >>> power(0, 5694)
        0
        >>> power(15, 5)
        759375
        >>> power(25429134286345234172354, 0)
        1
    """
    if y == 1:
       return x
    elif y == 0:
       return 1
    elif x == 0:
       return 0
    else:
       return x*power(x,y-1)
    
def sum_list(num_list):
    """
        precondition: takes a list of numbers
        postcondition: returns the sum of all numbers in the list.
        Examples:
        >>> sum_list([2,6,8,4,1]) 
        21
        >>> sum_list([6,9,7,-8,4,6]) 
        24
        >>> sum_list([6,9,7,-8,4,6,10,0,10]) 
        44
        >>> sum_list([6,9,7,-8,4,6,10,0,10,-40,100,6]) 
        110
    """
    if len(num_list)==1:
       return num_list[0]
    else:
       return num_list[0]+ sum_list(num_list[1:])
    
def is_prime(num, current):
    """
        precondition:   takes an integer num >=0 and current is given the value of 2
        postcondition:  returns a boolean value, True if the number is prime, False otherwise
        Examples:
        >>> is_prime(5, 2)
        True
        >>> is_prime(1, 2)
        False
        >>> is_prime(0, 2)
        False
        >>> is_prime(85, 2)
        False
        >>> is_prime(1019, 2)
        True
        >>> is_prime(61, 2)
        True
        >>> is_prime(62, 2)
        False
        >>> is_prime(2654, 2)
        False
    """
    if num == 1 or num == 0:
       return False
    if current >= math.sqrt(num):
        if num % current == 0:
            return False
        return True
    else:
        if num % current != 0:
            return True and is_prime(num, current+1)
        return False
           
def it_contains(num1, num2):
    """
        precondition:   takes two positive numbers
        postcondition:  returns True if all the digits of num1 appear in order among the digits of num2, False otherwise
        Examples:
        >>> it_contains(357, 12345678)
        True
        >>> it_contains(357, 12345357)
        True
        >>> it_contains(121, 21111211112)
        True
        >>> it_contains(753, 12345678)
        False
        >>> it_contains(357, 37)
        False
    """
    if num1 < 9:
        if num2>9:
            if num1%10 == num2%10:
                return True
            return it_contains(num1,num2//10)
        return False
    else:
        if num2>9:
            if num1%10 == num2%10:
                return True and it_contains(num1//10,num2//10)
            return it_contains(num1,num2//10)
        return False

def remove_evens(num_lst):
    """
        precondition: takes a list of numbers
        postcondition: removes all even numbers from the list, returning a new list with only the odd numbers.
        Examples
        Examples:
        >>> remove_evens([6, 8,7,65,6,4,6]) 
        [7, 65]
        >>> remove_evens([1,2,3,5,-8,4,89,4,7,5,1,4,8]) 
        [1, 3, 5, 89, 7, 5, 1]
        >>> remove_evens([2,4,6,8,10])                  
        []
        >>> remove_evens([6, 8,7,65,6,4,6, 7, 11, 12, 13]) 
        [7, 65, 7, 11, 13]
        >>> remove_evens([1,1,1,1,1,1,1,1]) 
        [1, 1, 1, 1, 1, 1, 1, 1]
    """
    if len(num_lst) == 1:
        if num_lst[0]%2 != 0:
            return [num_lst[0]]
        else:
            return []
    else:
        if num_lst[0]%2 != 0:
            return [num_lst[0]] + remove_evens(num_lst[1:])
        else:
            return remove_evens(num_lst[1:])
        
def run_tests_b():
  import doctest
  doctest.run_docstring_examples(remove_evens, globals(), name="HW2", verbose=True)

if __name__== "__main__":
  run_tests_b()
# LAB 3
# REMINDER: The work in this assignment must be your own original work and must be completed alone.
# All functions should NOT contain any for/while loops or global variables.
# Use recursion, otherwise no credit will be given
# No helper functions allowed!

def is_power_of(base, num):
    """
        >>> is_power_of(5, 625)  # pow(5, 4) = 5 * 5 * 5 * 5 = 625
        True
        >>> is_power_of(5, 1)    # pow(5, 0) = 1
        True
        >>> is_power_of(5, 5)    # pow(5, 1) = 5
        True
        >>> is_power_of(5, 15)   # 15 is not a power of 5 (it's a multiple)
        False
        >>> is_power_of(3, 9)
        True
        >>> is_power_of(3, 8)
        False
        >>> is_power_of(3, 10)
        False
        >>> is_power_of(1, 8)
        False
        >>> is_power_of(2, 0)    # 0 is not a power of any positive base.
        False
        >>> is_power_of(4, 16)
        True
        >>> is_power_of(4, 64)
        True
        >>> is_power_of(4, 63)
        False
        >>> is_power_of(4, 65)
        False
        >>> is_power_of(4, 32)
        False
        >>> is_power_of(1, 1)
        True
        >>> is_power_of(2,8)
        True
        >>> is_power_of(10,70)
        False
        >>> is_power_of(5, 125)
        True
        >>> is_power_of(5, 625)
        True
        >>> is_power_of(5, 3125)
        True
        >>> is_power_of(5, 15625)
        True
        >>> is_power_of(0, 0)
        False
        >>> is_power_of(0, 1)
        True
    """
    if num < base:
        if num == 1:
            return True
        return False
    elif base == 1:
        if base == num:
            return True
        return False
    elif base == 0:
        if num == 1:
            return True
        return False
    if num != 0:
        return is_power_of(base,num/base)
    return False

def cut(a_list):
    """
        >>> cut([7, 4, 0])
        [7, 4, 0]
        >>> myList=[7, 4, -2, 1, 9]
        >>> cut(myList)   # Found(-2) Delete -2 and 1
        [7, 4, 9]
        >>> myList
        [7, 4, -2, 1, 9]
        >>> cut([-4, -7, -2, 1, 9]) # Found(-4) Delete -4, -7, -2 and 1
        [9]
        >>> cut([-3, -4, 5, -4, 1])  # Found(-3) Delete -2, -4 and 5. Found(-4) Delete -4 and 1
        []
        >>> cut([5, 7, -1, 6, -3, 1, 8, 785, 5, -2, 1, 0, 42]) # Found(-1) Delete -1. Found(-3) Delete -3, 1 and 8. Found(-2) Delete -2 and 0
        [5, 7, 6, 785, 5, 0, 42]
	"""
    ## YOUR CODE STARTS HERE
    if len(a_list)==0:
        return []
    else:
        if a_list[0]<0:
            return cut(a_list[abs(a_list[0]):])
        return [a_list[0]]+cut(a_list[1:])

def right_max(num_list):
    """
        >>> right_max([3, 7, 2, 8, 6, 4, 5])
        [8, 8, 8, 8, 6, 5, 5]
        >>> right_max([1, 2, 3, 4, 5, 6])
        [6, 6, 6, 6, 6, 6]
        >>> right_max([1, 25, 3, 48, 5, 6, 12, 14, 89, 3, 2])
        [89, 89, 89, 89, 89, 89, 89, 89, 89, 3, 2]
        >>> right_max([31231333132312, 5152312, 3123, 31, 48, 5, 90, 12, 14, 89, 3, 2])
        [31231333132312, 5152312, 3123, 90, 90, 90, 90, 89, 89, 89, 3, 2]
    """
    ## YOUR CODE STARTS HERE
    if len(num_list) == 2:
        if num_list[0] > num_list[1]:
            return [num_list[0]] + [num_list[1]]
        return [num_list[1]] + [num_list[1]]
    return right_max(num_list[ :-2] + [max(num_list[-2: ])]) + [num_list[-1]]

def consecutive_digits(num):
    """
        >>> consecutive_digits(2222466666678)
        True
        >>> consecutive_digits(12345684562)
        False
        >>> consecutive_digits(122)
        True
        >>> consecutive_digits(11)
        True
        >>> consecutive_digits(10101101010)
        True
        >>> consecutive_digits(1010101010)
        False
        >>> consecutive_digits(221)
        True
    """
    if num<10:
        return False
    elif num%10 == num%100//10:
        return True
    return False or consecutive_digits(num//10)

def only_evens(num):
    """
        >>> only_evens(66112)
        662
        >>> only_evens(4386112)
        4862
        >>> only_evens(0)
        0
        >>> only_evens(357997555531)
        0
        >>> only_evens(13847896213354889741236)
        84862488426
    """
    
    ## YOUR CODE STARTS HERE

    if num < 10:
        if num%2==0:
            return num
        return 0
    else:
        if num%10%2 == 0:
            return num%10 + 10*only_evens(num//10)
        return only_evens(num//10)



def run_tests():
    import doctest

    #- Run tests in all docstrings
    #doctest.testmod(verbose=True)
    
    #- Run tests per function - Uncomment the next line to run doctest by function. Replace is_power_of with the name of the function you want to test
    doctest.run_docstring_examples(right_max, globals(), name='LAB3',verbose=True)

if __name__ == "__main__":
    run_tests()
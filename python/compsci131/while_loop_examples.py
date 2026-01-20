"""
Write the function get_sum(n) where n is a positive integer. 
Returns the sum of all the naturals numbers [1, n].

"""
def get_sum(n):
    """
        >>> get_sum(2)
        3
        >>> get_sum(3) 
        6
        >>> get_sum(6) 
        21
    """
    total = 0

    # from n to 1
    while n > 0:
        total += n
        n-=1

    return total

    # from 1 to n
    total = 0
    k = 0
    while n >= k:
        total += k
        k+=1
    return total



"""
Write the function is_prime(n) where n is a positive integer.
The function returns True if n is a prime number, False otherwise

x % y returns the remainder of x when divided by y

"""
def is_prime(n):
    """
        >>> is_prime(10)
        False
        >>> is_prime(7)
        True
        >>> is_prime(1)
        False
    """
    if n <= 1:
        return False
    
    k = 2
    while k < n:
        if n % k == 0:
            return False
        else:
            k+=1
    return True
    


"""
Write the function has_digit(n, k) that returns True 
if a positive number n has digit k False otherwise

"""
def has_digit(n, k):
    """
        >>> has_digit(81089, 1)
        True
        >>> has_digit(12, 7)
        False
    """
    while n > 0:
        digit = n % 10 
        if digit == k:
            return True
        else:
            n = n //10 #n //= 10
    return False




"""
Write the function called digit_sum(n) where n is an integer.
Function returns the sum of the digits of n.

"""
def digit_sum(n):
    """
        >>> digit_sum(29107)
        19
        >>> digit_sum(-456)
        15
        >>> digit_sum(0)
        0
    """
    n = abs(n)

    #if n < 0:
    #    n= -1*n    # n = -n
    total = 0
    while n > 0:
        digit = n % 10
        total += digit
        n //=10
    return total




"""
Write the function swap_digits(n) where n is a positive integer. 
The function returns a new integer whose value is similar to n's
but with each pair of digits swapped in order. 
If the number contains an odd number of digits, leave the leftmost digit in its original place.
"""

def swap_digits(n):
    """
        >>> swap_digits(482596) 
        845269
        >>> swap_digits(1234567) 
        1325476
    """
    result = 0
    power = 1

    while n//10!=0:
        last = n % 10    # 6
        sec_to_last = (n // 10) % 10   #9
        n = n // 100   # 4825
        result += (sec_to_last * power) + (last * power * 10)   #69
        power *=100
    result += n * power
    return result





def run_tests_d():
    import doctest

    # Run start tests in all docstrings
    #doctest.testmod(verbose=True)
    
    # Run start tests per function 
    doctest.run_docstring_examples(swap_digits, globals(), name='While loop Examples',verbose=True)   

if __name__ == "__main__":
    run_tests_d()

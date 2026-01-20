import math
def factorial_sum(num):
    """
        precondition: num is a positive number
        postcondtion: returns the sum of factorials for 1 to num
    
        >>> factorial_sum(5)      # 1! + 2! +3! + 4! + 5!
        153
        >>> factorial_sum(12) 
        522956313
        >>> factorial_sum(-9) 
        Traceback (most recent call last):
        ...
        AssertionError
    """
    assert num > 0

    sum = 0
    factorial = 1 
    while num >0:
        for i in range(1,num+1):
            factorial *= i
        sum += factorial
        factorial = 1
        num-=1
    return sum
       
def is_perfect_number_for(num):
    """
        precondition: num is a positive int
        postcondition: returns true if num is a perfect number

        >>> is_perfect_number_for(6)
        True
        >>> is_perfect_number_for(28)
        True
        >>> is_perfect_number_for(494)
        False
        >>> is_perfect_number_for(8128)
        True
    """
    total = 1
    for x in range(1,int(math.sqrt(num))+1):
        for i in range(num,int(math.sqrt(num)),-1):
            if x*i == num and x!= num and i!=num:
                total +=(x+i)
    if total == num:
       return True
    return False
 


def is_perfect_number_while(num):
    """
        precondition: num is a positive int
        postcondition: returns true if num is a perfect number

        >>> is_perfect_number_while(6)
        True
        >>> is_perfect_number_while(28)
        True
        >>> is_perfect_number_while(494)
        False
        >>> is_perfect_number_while(8128)
        True
    """
    def get_factor(num,k):
        while num > 0:
            if num%k == 0:
                return num//k
            num-=1
        
    counter = 1
    total = 0
    while counter <= int(math.sqrt(num)):
        factor = get_factor(num,counter)
        if counter != num and num%counter == 0:
            total += counter
            if factor!=num:
                total += factor
        counter+=1


    if total == num:
        return True
    return False


def is_unique(num,d):
  """
        >>> is_unique(123132, 5)
        False
        >>> is_unique(7264578364, 3)
        True
        >>> is_unique(444444, 4)
        False
        >>> is_unique(45, -4)
        Traceback (most recent call last):
        ...
        AssertionError
  """
  assert type(num)==int and type(d) == int and num > 0 and d > 0
  def howmany(num,d):  
    total = 0
    while num > 0:
            digit = num % 10 
            if digit == d:
                total+=1
                num //= 10
            else:
                num //= 10
    return total

  if howmany(num,d) == 1:
      return True
  return False

def get_num():
    """
        >>> get_num()
        42857
    """
    for x in range(10000,100000):
        leftadd = x+100000
        rightadd = (x*10)+1
        if leftadd == rightadd/3:
            return x
        
def run_tests_a():
  print("testing")
  #assert
  print("all tests are good")

def run_tests_b():
  import doctest
  #doctest.testmod(verbose=True)
  doctest.run_docstring_examples(is_perfect_number_while, globals(), name="HW2", verbose=True)
  

if __name__== "__main__":
  #run_tests_a()
  run_tests_b()
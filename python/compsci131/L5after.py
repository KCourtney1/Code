
def multiply(p1,p2):
    """
        precondition: p1 and p2 are a non-empty list of numbers
        postcondition: returns a new list representing the polynomial which is the product of the two

        >>> multiply([2,0,3], [4,5])    # (2x2 + 3)(4x + 5) = 8x3 + 10x2 + 12x + 15        
        [8, 10, 12, 15]
        >>> multiply([-9,6,1,2], [4,5,6]) 
        [-36, -21, -20, 49, 16, 12]
    """
                
    result = []
    result_len = len(p1)+len(p2)
    for i in range(result_len-1):
       result.append(0)

    for i in range(len(p1)):
       for j in range(len(p2)):
          result[i+j] += p1[i] * p2[j]

    return result
    
def non_destructive_remove(lst):
  """
      precondition: lst is an none empty list
      postcondition: returns new lst that removed all repeating values in lst
      Examples:
      >>> my_list = [5, 6, 8, 9, 5, 4, 1, 5, 1]                       
      >>> non_destructive_remove(my_list)
      [5, 6, 8, 9, 4, 1]
      >>> my_list                       
      [5, 6, 8, 9, 5, 4, 1, 5, 1]
  """
  new_lst = []
  for num in lst:
      if not num in new_lst:
        new_lst.append(num)        
  return new_lst

def destructive_remove(lst):
  """
      precondition: lst is an none empty list
      postcondition: returns new lst that removed all repeating values in lst
      Examples:
      Examples:
      >>> my_list = [5, 6, 8, 9, 5, 4, 1, 5, 1]
      >>> destructive_remove(my_list)     
      >>> my_list                              
      [5, 6, 8, 9, 4, 1]
  """
  i = 0
  while i < len(lst):
    k = i+1
    while k < len(lst):
      if lst[i] == lst[k]:
          del lst[k]
          k-=1
      k+=1
    i += 1

def title_case(s):
  """
      precondition: s us a none empty string 
      postcondition: returns string with first character in each word capitalized
      Example: 
      >>> title_case('we Are peNN state') 
      'We Are Penn State'
      >>> title_case('   we Are peNN state   ') 
      'We Are Penn State'
  """
  s = s.lower().split()
  new_s = []
  for word in range(len(s)):
    new_s.append(s[word][0].upper() + s[word][1:])
  return " ".join(new_s)
  
def alternating_sum(lst):
  """
      precondition: lst is a list of numbers 
      postcondition: returns the sum of lst with alternating addition and subtraction
      Examples:
      >>> alternating_sum([1, 5])         # 1 - 5
      -4.0
      >>> alternating_sum([1, 5, 17])    # 1 - 5 + 17
      13.0
      >>> alternating_sum([1, 5, 17, 4])  # 1 - 5 + 17 -4
      9.0
  """

  sum = 0.0
  for i in range(len(lst)):
    if i % 2 == 0:
      sum += lst[i]
    else: 
      sum -= lst[i]
  return sum

def sum_fold(lst):
  """
      precondition: lst is an none empty list of numbers
      postcondition:  returns the lst with Each element at position i becomes the sum up to and including that position.
      Examples:
      >>> my_list = [0,1,2,3,4] 
      >>> sum_fold(my_list) 
      >>> my_list          
      [0, 1, 3, 6, 10]
      >>> my_list = [5,2,-9,6]  
      >>> sum_fold(my_list)
      >>> my_list
      [5, 7, -2, 4]
  """
  new_lst = lst[:]
  for i in range(len(lst)):
    for k in range(i):
      lst[i] += new_lst[k]

def join_v2(delimiter, lst):
  """
      precodition:delimiter is the value to use for join, which is a list of strings, and lst a list of strings.
      postcondition: function returns a new string with the join value between each element in lst as follows: use the first element of the delimiter list for the first join, the second element for the second join, and so on, looping back to the first element once it exhausts the delimiter list.
      Examples:
      >>> join_v2(['+', '%'], ['This', 'is', 'a', 'list', 'of', 'words'])  
      'This+is%a+list%of+words'
      >>> join_v2(['+', '%'], ['we', 'are'])                              
      'we+are'
      >>> join_v2(['+', '%','-'], ['This', 'is', 'a', 'list', 'of','words', 'words', 'words', 'words', 'words'])  
      'This+is%a-list+of%words-words+words%words-words'
  """
  new_s = ""
  k = 0
  for i in range(len(lst)):
      if k == len(delimiter):
        k = 0
      if k == len(lst):
        new_s.strip()
      new_s += lst[i]+delimiter[k]
      k+=1
  for remove in delimiter:
    new_s = new_s.strip(remove)
  return new_s

def num_to_digit_loop(num,base):
  """
      precondition: num and base are positive integers
      postcondition: Return an empty list if base < 2 or num <= 0.
      Examples:
      >>> num_to_digit_loop(137, 10)
      [1, 3, 7]
      >>> num_to_digit_loop(137, 8)
      [2, 1, 1]
      >>> num_to_digit_loop(598, 2) 
      [1, 0, 0, 1, 0, 1, 0, 1, 1, 0]
      >>> num_to_digit_loop(654, 1) 
      []
      >>> num_to_digit_loop(654, 5)  
      [1, 0, 1, 0, 4]
  """
  lst = []
  if base<2 or num<=0:
    return lst
  lst.append(num%base)
  num//=base
  
  while num>0:
    lst.insert(0,num%base)
    num//=base
  return lst 

def dot_product(lst1,lst2):
  """
      precondition: both parameters are non-empty lists of numbers
      postcondition: returns the dot product of those lists.
      Examples:
      >>> dot_product([1,2,3], [4,5,6]) 
      32
      >>> dot_product([1,2,3], [4,5,6,7,8]) 
      32
      >>> dot_product([5,8,7,8], [4,5,6,7,8]) 
      158
      >>> dot_product([4,5,6,7,8],[5,8,7,8] )
      158
  """
  if len(lst1) > len(lst2):
    temp = lst1
    lst1 = lst2
    lst2 = temp

  sum = 0
  for i in range(len(lst1)):
    sum += lst1[i]*lst2[i]
  return sum

def find(char,seq):
  """
      precondition: char is a string of size 1 and seq is an iterable value.
      postcondition: returns an integer that represents the position of the first occurrence of char in seq. Return -1 when char is not present in seq
      Examples:
      >>> find('a', 'we are at home') 
      3
      >>> find('x', 'we are at home') 
      -1
      >>> find('at', ['we', 'are', 'at', 'home']) 
      2
  """
  for i in range(len(seq)):
    if seq[i] == char:
      return i
  return -1

def run_tests_b():
  import doctest
  #doctest.testmod(verbose=True)
  doctest.run_docstring_examples(num_to_digit_loop, globals(), name="HW2", verbose=True)

if __name__== "__main__":
  run_tests_b()
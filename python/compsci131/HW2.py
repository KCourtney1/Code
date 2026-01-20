import math

def intersect(x1,y1,r1,x2,y2,r2):
  """
      precondition: arguments are positve numbers
      postcondition: returns true if the two circles intersect and false otherwise

      >>> intersect(2, 3, 12, 15, 28, 10)
      False
      >>> intersect(3, 4, 5, 14, 18, 8)   
      False
      >>> intersect(-10, 8, 30, 14, -24, 10) 
      True
      >>> intersect(1, 1, 3, 5, 4, 2)        
      True
  """
  assert type(x1)==int and type(y1)==int and type(r1)==int and type(x2)==int and type(y2)==int and type(r2)==int, "preconditions not met"
  
  distance = math.sqrt(((x2-x1)**2)+((y2-y1)**2))
  if distance < r1 - r2 or distance<= r1+r2 or distance == 0:
    return True
  return False
  
def get_num(num,bound1,bound2):
  """
      precondition: arguments are numbers
      postcondition: returns num if > bound1 and < bound2, otherwise if num < bound1 return bound1 and if num > bound2 return bound2

      >>> get_num(1,3,5)  
      3
      >>> get_num(4,3,5)
      4
      >>> get_num(6,5,3)
      5
      >>> get_num(4.5, 3.5, 5.5)
      4.5
  """
  
  temp = bound2
  if bound1 > bound2:
    bound2 = bound1
    bound1 = temp

  if num > bound1 and num < bound2:
    return num
  elif num< bound1:
    return bound1
  elif num> bound2:
    return bound2

def how_many(qty):
  """
      precondition: qty is a positve number
      postcondition: returns smallest int number og cartons required to hold all the eggs, one carton holds 12 eggs

      >>> how_many(12) 
      1
      >>> how_many(5)  
      1
      >>> how_many(24) 
      2
      >>> how_many(6548) 
      546
  """
  assert type(qty)==int, "preconditions not met"
  
  if qty/12 < 1:
    return 1
  return round(qty/12)

def is_even_positive(num):
  """
      precondition: num is a numerical value
      postcondition: returns true if num is an int, and is positive, and is even
      
      >>> is_even_positive(12) 
      True
      >>> is_even_positive(12.0) 
      False
      >>> is_even_positive('hello') 
      False
      >>> is_even_positive(33)      
      False
      >>> is_even_positive(-12) 
      False
  """
  assert type(num) != list

  if type(num) == int and num%2 == 0 and num > 0:
    return True
  else:
    return False

def is_triangle(s1,s2,s3):
  """
      precondition: s1,s2,s3 are positive numerical values
      postcondition: returns true if such a triangle exists given sides, and false if the sum of two sides is not greater than the third side

      >>> is_triangle(3, 4, 5)
      True
      >>> is_triangle(2, 2, 5) 
      False
      >>> is_triangle(3, -4, 5) 
      False
  """
  assert type(s1)==int and type(s2)==int and type(s3)==int, "preconditions not met"
  
  if s1 + s2> s3:
    return True
  return False

def get_chinese_zodiac(year):
  """
      precondition: takes a positive year in the format XXXX
      postcondition: returns a string with the name of the animal that represents year

      >>> get_chinese_zodiac(2003)
      'sheep'
      >>> get_chinese_zodiac(2022) 
      'tiger'
      >>> get_chinese_zodiac(2023) 
      'rabbit'
      >>> get_chinese_zodiac(2020) 
      'rat'
      >>> get_chinese_zodiac(2021) 
      'ox'
      >>> get_chinese_zodiac(2031) 
      'pig'
  """
  assert type(year)== int, "preconditions not met"

  animal = ["monkey", "rooster", "dog", "pig", "rat", "ox", "tiger", "rabbit", "dragon", "snake", "horse", "sheep"]
  year = year%12
  return animal[year]

def is_close(num):
  if num > .50:
    return 1
  elif num <.50:
    return 0
  else:
    return .5

def get_tax(status,income):
  """
      precondition: integer value that represents filing status, and income is a numerical value that represents tacable income
      postcondition: returns a numerical value of tax for the tacable income based on filing status, returns the string "invalid information" if the arguments don't follow specifications

      >>> get_tax(1, 20000)
      2194.5
      >>> get_tax(1, 600000) 
      184955.0
      >>> get_tax(2, 220000) 
      40471.0
      >>> get_tax(3, 990000) 
      333574.5
      >>> get_tax(9, 220000) 
      'Invalid information'
      >>> get_tax(1, 20000.87)
      2194.6044
  """
  
  tax = 0
  if status == 1:
    if income > 539900:
      tax+= (income-539900)*.37
      tax+= ((10275-0)*.10+(41775-10275)*.12+(89075-41775)*.22+(170050-89075)*.24+(215950-170050)*.32+(539900-215950)*.35)
    elif income >= 215950:
      tax+= (income-215950)*.35
      tax+= ((10275-0)*.10+(41775-10275)*.12+(89075-41775)*.22+(170050-89075)*.24+(215950-170050)*.32)
    elif income >= 170050:
      tax+= (income-170501)*.32
      tax+= ((10275-0)*.10+(41775-10275)*.12+(89075-41775)*.22+(170050-89075)*.24)
    elif income >= 89075:
      tax+= (income-89075)*.24
      tax+= ((10275-0)*.10+(41775-10275)*.12+(89075-41775)*.22)
    elif income >= 41775:
      tax+= (income-41775)*.22
      tax+= ((10275-0)*.10+(41775-10275)*.12)
    elif income >= 10275:
      tax+= (income-10275)*.12
      tax+= ((10275-0)*.10)
    else:
      tax += (income)*.10
  elif status == 2:
    if income > 647850:
      tax+= (income-647850)*.37
      tax+= ((20550-0)*.10+(83550-20550)*.12+(178150-83550)*.22+(340100-178150)*.24+(431900-340100)*.32+(647850-431900)*.35)
    elif income >= 431900:
      tax+= (income-431900)*.35
      tax+= ((20550-0)*.10+(83550-20550)*.12+(178150-83550)*.22+(340100-178150)*.24+(431900-340100)*.32)
    elif income >= 340100:
      tax+= (income-340100)*.32
      tax+= ((20550-0)*.10+(83550-20550)*.12+(178150-83550)*.22+(340100-178150)*.24)
    elif income >= 178150:
      tax+= (income-178150)*.24
      tax+= ((20550-0)*.10+(83550-20550)*.12+(178150-83550)*.22)
    elif income >= 83550:
      tax+= (income-178150)*.22
      tax+= ((20550-0)*.10+(83550-20550)*.12)
    elif income >= 20550:
      tax+= (income-20550)*.12
      tax+= ((20550-0)*.10)
    else:
      tax += (income)*.10
  elif status == 3:
    if income > 323925:
      tax+= (income-323925)*.37
      tax+= ((10275-0)*.10+(41775-10275)*.12+(89075-41775)*.22+(170050-89075)*.24+(215950-170050)*.32+(323925-215950)*.35)
    elif income >= 215950:
      tax+= (income-215950)*.35
      tax+= ((10275-0)*.10+(41775-10275)*.12+(89075-41775)*.22+(170050-89075)*.24+(215950-170050)*.32)
    elif income >= 170050:
      tax+= (income-170501)*.32
      tax+= ((10275-0)*.10+(41775-10275)*.12+(89075-41775)*.22+(170050-89075)*.24)
    elif income >= 89075:
      tax+= (income-89075)*.24
      tax+= ((10275-0)*.10+(41775-10275)*.12+(89075-41775)*.22)
    elif income >= 41775:
      tax+= (income-41775)*.22
      tax+= ((10275-0)*.10+(41775-10275)*.12)
    elif income >= 10275:
      tax+= (income-10275)*.12
      tax+= ((10275-0)*.10)
    else:
      tax += (income)*.10
  elif status == 4:
    if income > 539900:
      tax+= (income-539900)*.37
      tax+= ((14650-0)*.10+(55900-14650)*.12+(89050-55900)*.22+(170050-89050)*.24+(215950-170050)*.32+(539900-215950)*.35)
    elif income >= 215950:
      tax+= (income-215950)*.35
      tax+= ((14650-0)*.10+(55900-14650)*.12+(89050-55900)*.22+(170050-89050)*.24+(215950-170050)*.32)
    elif income >= 170050:
      tax+= (income-170501)*.32
      tax+= ((14650-0)*.10+(55900-14650)*.12+(89050-55900)*.22+(170050-89050)*.24)
    elif income >= 89050:
      tax+= (income-89050)*.24
      tax+= ((14650-0)*.10+(55900-14650)*.12+(89050-55900)*.22)
    elif income >= 55900:
      tax+= (income-55900)*.22
      tax+= ((14650-0)*.10+(55900-14650)*.12)
    elif income >= 14650:
      tax+= (income-14650)*.12
      tax+= ((14650-0)*.10)
    else:
      tax += (income)*.10
  else:
    return "Invalid information"
  return tax
      
def temp_sum(start,end):
  """
      precondition: start and end are a numerical values
      postcondition: returns a numerical sum of the equivalent Fahrenheit temperature for the Celsius temperatures from start to end (inclusive) in increments of 5 degrees.

      >>> temp_sum(10,30)
      340.0
      >>> temp_sum(50,3000) 
      1641207.0
      >>> temp_sum(12,73)   
      1398.8000000000002
  """
  assert type(start)==int and type(end)== int, "preconditions not met"

  total = 0.0
  for i in range(start,end+1,5):
    total = total + (i*(9/5)+32)
  return total

def estimate(billion):
  """
      precondition: numerical vlaue that represents the number of billions 
      postcondition: retuns the number of years when the population will reach billion

      >>> estimate(8)
      2024
      >>> estimate(10) 
      2044
      >>> estimate(11.5) 
      2057
  """
  assert type(billion)== int or type(billion)==float,"preconditions not met"
  
  year = 2011
  pop = 7
  
  while pop <= billion:
    pop = pop+(pop*.011)
    year += 1

  return year

def summary(num_lst):
  """
      precondition: num_lst is a list
      postcondition: returns three values: the number of positive and negative values present in the list and the average of the elements in the list (not counting zeros).

      >>> summary([1, 3, 5, -19])
      (3, 1, -2.5)
      >>> summary([1,-2, 5, 5, 0, 1, 3, 5, 9, -10, 0, 25]) 
      (8, 2, 4.2)
  """
  assert type(num_lst) == list, "preconditions not met"

  pos = 0
  neg = 0
  avg = 0
  for x in num_lst:
    avg += x
    if x > 0:
      pos += 1
    elif x < 0:
      neg += 1

  return pos,neg,(avg/(pos+neg))

def is_valid(num_lst):
  """
      precondition: num_lst is a list
      postcondition: return True if the list of numbers represents a valid credit card number, False otherwise, according to the following verification method

      >>> is_valid([5,8,6,6,7,9,3,6,1,0,0,2,4,4]) 
      True
      >>> is_valid([5,8,6,6,7,9,3,6,1,0,0,2,4,4,9,6]) 
      False
      >>> is_valid([5,8,6,6,7,3,6,1,0,2,4,4,9,6])     
      False
  """
  assert type(num_lst) == list, "preconditions not met"

  sum = 0
  for x in range(len(num_lst)):
    if x%2 == 0:
      x = num_lst[x]*2
      if x > 9:
        x -= 9
      sum += x 
    elif x%2 != 0:
      x = num_lst[x]
      sum += x 
  if sum%10 == 0:
    return True
  return False

def is_sorted(num_lst):
  """
      precondition: num_lst is a list
      postcondition: returns True if the list is sorted (either ascending or descending order), False otherwise

      >>> is_sorted([1,2,3,4,65]) 
      True
      >>> is_sorted([1,2,-3,4,65]) 
      False
      >>> is_sorted([5,4,3,2,1])   
      True
      >>> is_sorted([5,4,-3,2,1])   
      False
      >>> is_sorted([5,4,2,1,65])   
      False
  """
  assert type(num_lst) == list, "preconditions not met"

  ascending = True
  descending = True
  for i in range(1,len(num_lst)):
    if num_lst[i-1] > num_lst[i]:
      ascending = False
    if num_lst[-i-1] < num_lst[-i]:
      descending = False
  if ascending or descending:
    return True
  return False

def classify(num):
  """
      precondition: num is a numerical number
      postcondition: function prints (not returns) a string to classify each number in the range 2 to num (inclusive) as abundant, deficient or perfect using the format "value is ________".

      >>> classify(25)
      2 is deficient
      3 is deficient
      4 is deficient
      5 is deficient
      6 is perfect
      7 is deficient
      8 is deficient
      9 is deficient
      10 is deficient
      11 is deficient
      12 is abundant
      13 is deficient
      14 is deficient
      15 is deficient
      16 is deficient
      17 is deficient
      18 is abundant
      19 is deficient
      20 is abundant
      21 is deficient
      22 is deficient
      23 is deficient
      24 is abundant
      25 is deficient
  """
  assert type(num) == int, "preconditions not met"

  for x in range(2,num+1):
    propersum = 0
    for i in range(1,num):
      if x%i == 0:
        if i != x:
          propersum += i
    if propersum > x:
      print(f"{x} is abundant")
    elif propersum < x:
      print(f"{x} is deficient")
    else:
      print(f"{x} is perfect")
    



def has_digit(num,k):
  """
      precondition: num and k a numerical values
      postcondition: returns True if k is a digit in num

      >>> has_digit(-9541, 9)
      True
      >>> has_digit(9541, 9)
      True
      >>> has_digit(951, 4)
      False
      >>> has_digit(951.45, 9)
      False
      >>> has_digit(45, 9.75)  
      False
  """
  if type(num) == float:
    return False
  if num < 0:
    num = abs(num) 
  while num > 0:
        digit = num % 10 
        if digit == k:
            return True
        else:
            num //= 10
  return False

def single_count(num):
  """
      precondition: num is a positive integer
      postcondition: returns the single count of digits in num

      >>> single_count(8675309)       # All are unique
      7
      >>> single_count(1313131)       # 1 and 3
      2
      >>> single_count(13173131)      # 1, 3, and 7
      3
      >>> single_count(10000)         # 0 and 1
      2
      >>> single_count(101)           # 0 and 1
      2
      >>> single_count(10)            # 0 and 1
      2
  """
  total = 0
  while num > 0:
    digit = num % 10 
    if has_digit(num//10,digit)==False:
      total += 1
    num//=10
  return total

def count_digits(num):
    assert type(num)==int
    digits = 0
    num = abs(num)
    while num > 0:
        digits += 1
        num//=10
    

def is_mirrored(num):
  """
      precondition: num is a positive integer
      postcondition: returns True if num is a mirrored number and False otherwise.

      >>> is_mirrored(88)
      True
      >>> is_mirrored(246246) 
      True
      >>> is_mirrored(24624)  
      False
      >>> is_mirrored(59)    
      False
      >>> is_mirrored(5995) 
      False
  """
  num = abs(num)

  digits = 0
  num_temp = num
  while num_temp > 0: 
      digits += 1
      num_temp//=10
  
  if digits%2 != 0:
    return False
  
  midpoint = digits//2
  last = num%(10**midpoint)
  first = num//(10**(midpoint))

  if first == last:
    return True
  return False

def all_factors(num):
  """
      precondition: num is a positive integer
      postcondition: returns True if num is a (possibly-negative) integer with exactly 3 unique digits (so no two digits are the same), where each of the digits is a factor of num. In all other cases, the function returns False (without crashing).

      >>> all_factors(612)  
      True
      >>> all_factors(-612)
      True
      >>> all_factors(2612) 
      False
      >>> all_factors(602)  
      False
      >>> all_factors(62)  
      False
      >>> all_factors('hello') 
      False
      >>> all_factors(612.0)   
      False
  """
  
  if type(num) != int:
    return False
  num = abs(num)
  factorunique = False
  if single_count(num)!=3:
    return False
  while num > 0:
    digit = num%10
    if has_digit(num//10,digit):
      return False
    if digit!=0 and num%digit == 0:
      factorunique = True
    else:
      return False
    num//=10
  return factorunique


def run_tests_a():
  print("testing")
  #assert
  print("all tests are good")

def run_tests_b():
  import doctest
  #doctest.testmod(verbose=True)
  doctest.run_docstring_examples(is_mirrored, globals(), name="HW2", verbose=True)
  

if __name__== "__main__":
  #run_tests_a()
  run_tests_b()
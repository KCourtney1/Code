

def reverse_sentence(s):
    """
        precondition: s is an non-empty string
        postcondition: returns reversed sentence in a string only reversing if s > 1 word
        >>> reverse_sentence('hello') 
        'hello'
        >>> reverse_sentence('we are penn state') 
        'state penn are we'
        >>> reverse_sentence('you are my sunshine') 
        'sunshine my are you'
        >>> reverse_sentence('this is not reverse') 
        'reverse not is this'
        >>> reverse_sentence('this is another test case')
        'case test another is this'
    """
    s = s.split()
    result = []
    for word in range(-1,-len(s)-1,-1):
       result += [s[word]]
    return " ".join(result)

def get_second(s):
   """
        precondition: s is an non-empty string with words seperated by at least 2 commas
        postcondition: returns the second word in s, with any leading or trailing spaces from the second word removed
        >>> get_second('mouse, cat, dog, pig, lion') 
        'cat'
        >>> get_second('apple,          pear        , banana') 
        'pear'
        >>> get_second('1, 2, 3, 4, 5')
        '2'
        >>> get_second('chicken, cow, ten, keyboard, mouse')
        'cow'
   """
   s = s.split(",")
   return s[1].strip()

def rotate_left(s,n):
    """
        precondition: s is a string and a n is an integer
        postcondition: retuens s rotated n positions to the left if pos and right in neg
        >>> rotate_left('xyzw', 1) 
        'yzwx'
        >>> rotate_left('xyzw', 2) 
        'zwxy'
        >>> rotate_left('xyzw', 3) 
        'wxyz'
        >>> rotate_left('xyzw', -1) 
        'wxyz'
        >>> rotate_left('xyzw', -2) 
        'zwxy'
        >>> rotate_left('xyzw', -3) 
        'yzwx'
        >>> rotate_left('abcd', -3) 
        'bcda'
        >>> rotate_left('abcd', 1) 
        'bcda'
    """
    
    result = ""
    if n > 0:
        temp = s[n:]
        result += temp + s[0:n]
    else:
        temp = s[n:]
        result += temp + s[0:n] 
    return result

def is_balanced(s):
    """
        precondtion: s is a string
        postcondition: returns true if s has balanced parenthesis false otherwise
        >>> is_balanced("( ( ( ) ( ) ) ( ) )")
        True
        >>> is_balanced("( ) )")
        False
        >>> is_balanced("(())(())())(")
        False
        >>> is_balanced("())(")         
        False
        >>> is_balanced("(((())))()") 
        True
        >>> is_balanced(")))((()))")
        False
        >>> is_balanced("((()())(())(())(()))(())")
        True
    """
    #find open then look for closed if found remove both, if cant find closed return false
    def remove_spaces():
        while " " in s:
            if " " in s:
                s.remove(" ")
    s = list(s)
    remove_spaces()

    while len(s)!=0:
        if "(" in s[0]:
            s.remove(")")
            s.remove("(")  
        else:
            return False
    return True

def find(char, s, start):
    """
        precondition:  takes a string of size 1, char, a string, s, and a positive integer start as input
        postcondition: returns the index of the first occurrence of char in s starting from start. If char is not found or the s is empty, return -1.
        >>> find('p', 'hello', 0) 
        -1
        >>> find('e', 'hello', 2) 
        -1
        >>> find('e', 'hello', 0) 
        1
        >>> find('l', 'hello', 1) 
        2
        >>> find('l', 'hello', 3) 
        3
        >>> find('f', 'aaaahhhhaaaahhhhfggggaaasss', 15) 
        16
        >>> find('I', 'I cant think of a test case', 10) 
        -1
    """
    for i in range(start,len(s)):
        if s[i]==char:
            return i
    return -1

def find_first_vowel(s):
    """
        >>> find_first_vowel('hello')   
        1
        >>> find_first_vowel('drone') 
        2
        >>> find_first_vowel('r2d2')  
        4
        >>> find_first_vowel('yummy')   
        1
        >>> find_first_vowel('dry')   
        2
        >>> find_first_vowel('yyummy')   
        1
        >>> find_first_vowel('dyry')   
        1
    """
    vowels = "aeiouy"
    first = len(s)
    for char in vowels:
        if s[0] == "y":
            hasvowle = find(char,s,1)
            if hasvowle < first and hasvowle != -1:
                first = hasvowle
        else:
            hasvowle = find(char,s,1)
            if hasvowle < first and hasvowle != -1:
                first = hasvowle
    return first

def get_pig_latin(s):
    """
        precondtion: s is a non-empty string of lowercase letters
        postcondition: returns a string that represents s in Pig Latin form
        >>> get_pig_latin('ortogonal') 
        'ortogonalhay'
        >>> get_pig_latin('quacking')
        'ackingquay'
        >>> get_pig_latin('blue')
        'ueblay'
        >>> get_pig_latin('dry')
        'ydray'
        >>> get_pig_latin('kmr')
        'kmray'
        >>> get_pig_latin('red')
        'erday'
        >>> get_pig_latin('chiken')
        'iechknay'
    """
    vowels = "aeiouy"
    pig_latin = ""
    end = ""

    if s[0]== "q":
        end += "quay"
        s = s[2:]
    elif s[0] in vowels:
        end+= "hay"

    if not s[0] in vowels:
        s = list(s)
        while len(s) != 0:
            first_vowels  = find_first_vowel(s)
            if first_vowels != len(s):
                pig_latin += s[first_vowels]
                del s[first_vowels]
            else:
                end += s[0]
                del s[0]
        end += "ay"
    else:
        pig_latin = s
    return pig_latin + end

def binary_to_decimal(lst):
    """
        precondition:that takes a list of 0s and 1s lst as input.
        postcondition: returns the integer represented by reading the list from left to right
        >>> binary_to_decimal([1, 0]) 
        2
        >>> binary_to_decimal([1, 0, 1, 1]) 
        11
        >>> binary_to_decimal([1, 1, 0, 1]) 
        13
        >>> binary_to_decimal([1, 1, 1, 1,1, 1, 1, 1,1, 1, 1, 1,1, 1, 1, 1,1, 1, 1, 1]) 
        1048575
        >>> binary_to_decimal([1, 1, 1, 1,1, 1, 1, 1,1, 1, 1, 1,1, 1, 1, 1,1, 1, 1, 1,1, 1, 1, 1,1, 1, 1, 1,1, 1, 1, 1,1, 1, 1, 1,1, 1, 1, 1,1, 1, 1, 1,1, 1, 1, 1,1, 1, 1, 1,1, 1, 1, 1,1, 1, 1, 1]) 
        1152921504606846975
    """
    power = len(lst)
    num = 0
    for number in lst:
        power-=1
        num += number*(2**power) 
    return num

def get_largest(s):
    """
        precondition: that takes a string s as input, numbers in the text are non-negative integers and that numbers are always composed of consecutive digits
        postcondition: returns highest int number in s
        >>> get_largest("I have 3 dogs, 77 cats, and 4 birds!")  
        77
        >>> get_largest("I have animals in my house")          
        >>> get_largest("I have animals in my house") is None
        True
        >>> get_largest("this 1203 is 843 - 5 - 52387 not a test")
        52387
        >>> get_largest("what 578134957 are tests 58634295032")
        58634295032
    """
    def remove_str(s):
        s = s.split()
        numbers = "1234567890"
        result = []
        for item in s:
            if item[0]in numbers:
                result += [int(item)]
        return result
            
    result = remove_str(s)
    result.sort()
    if len(result)!= 0:
        return result[-1]
    
def max_in_window(lst, w):
    """
        precondition: that takes a list of numbers lst and a positive integer w as input
        precondition: function returns a list that contains the maximum value of each of the sliding windows without destroying the original list.
        >>> max_in_window([2, 5, 12, 3, 4], 2)
        [5, 12, 12, 4]
        >>> max_in_window([1, 3, 5, 1, 2, 4, 7, 8], 4)
        [5, 5, 5, 7, 8]
        >>> max_in_window([1, 3, 0, 3, 5, 3, 6, 2, 8], 3)
        [3, 3, 5, 5, 6, 6, 8]
        >>> max_in_window([1,1,2,2,3,4,5],1)
        [1, 1, 2, 2, 3, 4, 5]
        >>> max_in_window([1,1,2,2,3,4,5,6,1,2,2,3,4,5,6],2)
        [1, 2, 2, 3, 4, 5, 6, 6, 2, 2, 3, 4, 5, 6]
        >>> max_in_window([1,2,3,4,5,6,7,8,9,10],10)
        [10]
    """
    window_largest = []
    for i in range(len(lst)-w//2):
        window = lst[i:i+w]
        if len(window) == w:
            window.sort()
            window_largest.append(window[-1])
    return window_largest

def merge_lists(lst1, lst2):
    """
        precondition: lst1 and lst 2 are list of numbers in ascending order
        postcondition return a list of size len(lst1) + len(lst2) that is sorted in ascending order.
        >>> merge_lists([1,2,3,4], [5,6,7,8,9,10,11])
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        >>> merge_lists([-5,-4,-1], [0, 9])           
        [-5, -4, -1, 0, 9]
        >>> merge_lists([3], [0, 1, 3, 5, 8]) 
        [0, 1, 3, 3, 5, 8]
        >>> merge_lists([1,2,3,4], [4, 5, 5, 5,6,7,8,9,10,11]) 
        [1, 2, 3, 4, 4, 5, 5, 5, 6, 7, 8, 9, 10, 11]

        >>> merge_lists([1,2,3,4,5,5,5,13], [5,6,7,8,9,10,11,12,154])
        [1, 2, 3, 4, 5, 5, 5, 5, 6, 7, 8, 9, 10, 11, 12, 13, 154]
        >>> merge_lists([5012], [5,6,7,8,9,10,11,12, 15, 25, 90, 154])
        [5, 6, 7, 8, 9, 10, 11, 12, 15, 25, 90, 154, 5012]
    """
    i = 0
    j = 0
    merged = []
    while len(lst1) > i and len(lst2) >j:
        if lst1[i] < lst2[j]:
            merged.append(lst1[i])
            i+=1
        else:
            merged.append(lst2[j])
            j+=1
    if len(lst1)>i:
        for num in range(i,len(lst1)):
            merged.append(lst1[num])
    if len(lst2)>j:
        for num in range(j,len(lst2)):
            merged.append(lst2[num])
    return merged
    
def move_to_back(lst, values):
    """
        precondition: takes two lists, lst and values, as input
        postcondition: The function mutates lst so that each element of lst that appears in values moves to the end of lst in the order that they appear in values
        >>> my_lst = [2, 3, 3, 4, 1, 5]
        >>> move_to_back(my_lst, [3])                
        >>> my_lst                     
        [2, 4, 1, 5, 3, 3]
        >>> my_lst = [2, 3, 3, 4, 1, 5]
        >>> move_to_back(my_lst, [2, 3])             
        >>> my_lst
        [4, 1, 5, 2, 3, 3]
        >>> my_lst = [2, 3, 3, 4, 1, 5]
        >>> move_to_back(my_lst, [3, 2])
        >>> my_lst
        [4, 1, 5, 3, 3, 2]
        >>> my_lst = [2, 3, 3, 4, 1, 5]
        >>> move_to_back(my_lst, [4, 1])
        >>> my_lst
        [2, 3, 3, 5, 4, 1]
        >>> my_lst = [15, 25, 15, 5, 5, 5]
        >>> move_to_back(my_lst, [25, 0])
        >>> my_lst
        [15, 15, 5, 5, 5, 25]
    """
    while len(values)!= 0:
        i = 0
        stop = 0
        while stop < len(lst):
            if lst[i] == values[0]:
                temp = lst[i]
                del lst[i]
                lst.append(temp)
            else:
                i+=1
            stop += 1 
        del values[0]

def joint_lst(lsts):
    """
        precondition: that takes a 2D list, lsts as input, where each inner list contains numbers only
        postcondition: returns a new list with all the numbers that appear in all the lists in lsts
        >>> joint_lst([[1, 2, 3], [1, 3, 5], [5, 3, 1]])
        [1, 3]
        >>> joint_lst([[75.5, 1, 2, 3], [1, 3, 5], [0, 5, 9, 3, 1, -96, 8, 1]])
        [1, 3]
        >>> joint_lst([[1, 2, 3], [4, 5], [7, 8, 9, 10], [6, 89]])
        []
        >>> joint_lst([[1, 2, 3], [4, 1, 5], [7, 8, 1, 9, 10], [1, 6, 89]])
        [1]
        >>> joint_lst([[1, 2, 3, 100], [4, 1, 5, 100], [7, 8, 1, 9, 10, 100], [1, 6, 89, 100]])
        [1, 100]
    """
    
    result = []
    if len(lsts) == 2:
        similar = []
        for num in lsts[0]:
            if num in lsts[1]:
                similar.append(num)
        return similar
    else:
        similar = joint_lst(lsts[1:])
        for num in lsts[0]:
            if num in similar:
                result.append(num)
        return result


def num_holidays(lsts):
    """
        precondition: takes a 2D list of holidays, lsts as input. 
        postcondition: returns the number of days off, that has no duplicate holidays and no overlapping holidays
        >>> summer_23 = [["Memorial Day", ["May", 29]], ["Juneteenth", ["Jun", 19]], ["Independence Day", ["July", 4]]] 
        >>> num_holidays(summer_23)
        3
        >>> fall_23 = [["Labor Day", ["Sep", 4]], ["Thanksgiving", ["Nov", 20], ["Nov", 24]]]
        >>> num_holidays(fall_23)
        6
        >>> fall_23 = [["Labor Day", ["Sep", 4], ["Sep", 30]], ["Thanksgiving", ["Nov", 20], ["Nov", 24]]]
        >>> num_holidays(fall_23)
        32
        >>> fall_23 = [["chrismas", ["dec", 23], ["dec", 30]], ["Thanksgiving", ["Nov", 20], ["Nov", 24]]]
        >>> num_holidays(fall_23)
        13
    """
    daysoff = []
    for item in lsts:
        day_range = []
        for day in range(1,len(item)):
            day_range.append(item[day][1])
        daysoff.append(day_range)

    totaldaysoff = 0
    for lst in daysoff:
        if len(lst)>1:
            totaldaysoff += lst[1]-(lst[0]-1)
        else:
            totaldaysoff += 1
    return totaldaysoff

def invert_dict(d):
    """
        precondition: takes a dictionary, d as input. d are never lists.
        postcondition: returns the new inverted dictionary.
        >>> invert_dict({'one':1, 'two':2,  'three':3, 'four':4})
        {1: 'one', 2: 'two', 3: 'three', 4: 'four'}
        >>> invert_dict({'one':1, 'two':2, 'uno':1, 'dos':2, 'three':3})
        {1: ['one', 'uno'], 2: ['two', 'dos'], 3: 'three'}
        >>> invert_dict({'123-456-78':'Sara', '987-12-585':'Alex', '258715':'sara', '00000':'Alex'}) 
        {'Sara': '123-456-78', 'Alex': ['987-12-585', '00000'], 'sara': '258715'}
        >>> invert_dict({'one':1, 'un':1, 'uno':1, 'eins':1, 'um':1})
        {1: ['one', 'un', 'uno', 'eins', 'um']}
        >>> invert_dict({'one':1})
        {1: 'one'}
    """
    invert_d = {}
    for key , Value in d.items():
        if Value in invert_d:
            if type(invert_d[Value])!=list:
                invert_d[Value] = [invert_d[Value]]
            invert_d[Value] += [key]
        else:
            invert_d[Value] = key
    return invert_d

def invert_dict_2(d):
    """
        precondition: that takes a dictionary, d as input.
        postcondition: returns the new inverted dictionary. dictionary that is the invert of d such that original key:value pairs i:j are now related j:i, but when there are nonunique values (j's) in d, the j:i pair is not added into the inverted dictionary. 
        >>> invert_dict_2({'one':1, 'two':2,  'three':3, 'four':4})
        {1: 'one', 2: 'two', 3: 'three', 4: 'four'}
        >>> invert_dict_2({'one':1, 'two':2, 'uno':1, 'dos':2, 'three':3})
        {3: 'three'}
        >>> invert_dict_2({'123-456-78':'Sara', '987-12-585':'Alex', '258715':'sara', '00000':'Alex'}) 
        {'Sara': '123-456-78', 'sara': '258715'}

        >>> invert_dict_2({'one':1, 'two':2, 'uno':1, 'dos':2, 'three':3, 'tres':3})
        {}
        >>> invert_dict_2({'two':2, 'uno':1, 'dos':2, 'three':3,})
        {1: 'uno', 3: 'three'}
    """
    invert_d = {}
    for key , Value in d.items():
        count = 0
        for _ , Value2 in d.items():
            if Value2 == Value:
                count += 1

        if count == 1:
            invert_d[Value] = key
    return invert_d

def selecting(employees, hired):
    """
        precondition: dictionary of employees and a list of hired employees as input
        postcondition: returns a new dictionary that consists only of the key:value pairs whose key is in the hired list. It does not mutate the original dictionary.
        >>> my_employees = {'Alice': 'Engineer', 'Bob': 'Manager', 'Carol': 'Sales'}
        >>> hired_emp = ['Alice', 'Bob']
        >>> selecting(my_employees, hired_emp)
        {'Alice': 'Engineer', 'Bob': 'Manager'}
        >>> my_employees
        {'Alice': 'Engineer', 'Bob': 'Manager', 'Carol': 'Sales'}

        >>> my_employees = {'Alice': 'Engineer', 'Bob': 'Manager', 'Carol': 'Sales', 'kyle': 'The Big Bucks'}
        >>> hired_emp = ['Alice', 'Bob', 'kyle']
        >>> selecting(my_employees, hired_emp)
        {'Alice': 'Engineer', 'Bob': 'Manager', 'kyle': 'The Big Bucks'}
        >>> my_employees
        {'Alice': 'Engineer', 'Bob': 'Manager', 'Carol': 'Sales', 'kyle': 'The Big Bucks'}
    """
    hired_d = {}
    for key , Value in employees.items():
        if key in hired:
            hired_d[key] = Value
    return hired_d

def count_words(s):
    """
        precondition: s is a string.
        postcondition: returns a dictionary whose keys are words in s, and values their word counts. If a string is not provided as an input, the function must return the string "Invalid input".
        >>> article='''
        ... Two new vents from the erupting Kilauea volcano on Hawaii 
        ... prompted officials on Tuesday afternoon to order the immediate evacuation of 
        ... residents remaining in Lanipuna Gardens. All 1,700 residents of Leilani Estates, 
        ... as well as the smaller Lanipuna, had previously been ordered to evacuate. 
        ... But that does not mean they all have. '''
        >>> count_words(article)
        {'two': 1, 'new': 1, 'vents': 1, 'from': 1, 'the': 3, 'erupting': 1, 'kilauea': 1, 'volcano': 1, 'on': 2, 'hawaii': 1, 'prompted': 1, 'officials': 1, 'tuesday': 1, 'afternoon': 1, 'to': 2, 'order': 1, 'immediate': 1, 'evacuation': 1, 'of': 2, 'residents': 2, 'remaining': 1, 'in': 1, 'lanipuna': 2, 'gardens': 1, 'all': 2, 'leilani': 1, 'estates': 1, 'as': 2, 'well': 1, 'smaller': 1, 'had': 1, 'previously': 1, 'been': 1, 'ordered': 1, 'evacuate': 1, 'but': 1, 'that': 1, 'does': 1, 'not': 1, 'mean': 1, 'they': 1, 'have': 1}
        >>> count_words(55)
        'Invalid input'
        >>> count_words([3.5,6])
        'Invalid input'
    """
    def removePunctuation(word):
        word = list(word)
        Punctuation = ",.?;'"
        for char in Punctuation:
            if char in word:
                word.remove(char)
        return "".join(word)
    
    def is_number(word):
        if word[0] in "1234567890":
            return True
        return False
    
    if type(s) != str:
        return "Invalid input"
    
    s = s.split()
    word_count = {}
    for word in s:
        word = removePunctuation(word.lower())
        if not is_number(word):
            if word in word_count :
                word_count[word] += 1
            else:
                word_count[word] = 1
    return word_count

def run_tests_b():
  import doctest
  doctest.run_docstring_examples(invert_dict_2, globals(), name="HW2", verbose=True)
  
if __name__== "__main__":
  run_tests_b()
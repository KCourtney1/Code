# HW1
# REMINDER: The work in this assignment must be your own original work and must be completed alone.
import math

def get_path(file_name):
    """
        Returns a string with the absolute path of a given file_name located in the same directory as this script

        # Do not modify this function in any way

        >>> get_path('words.txt')   # HW1.py and words.txt located in HW1 folder
        'G:\My Drive\CMPSC132\HW1\words.txt'
    """
    import os
    target_path = os.path.join(os.path.dirname(__file__), file_name)
    return target_path

def rectangle(perimeter,area):
    """
        >>> rectangle(14, 10)
        5
        >>> rectangle(12, 5)
        5
        >>> rectangle(25, 25)
        False
        >>> rectangle(50, 100)
        20
        >>> rectangle(11, 5)
        False
        >>> rectangle(11, 4)
        False
    """
    #- YOUR CODE STARTS HERE
    h = (perimeter + math.sqrt(perimeter**2-16*area))/4
    w = area/h
    if int(h)*int(w) == area and h%1 == 0:
        return int(h)
    else:
        return False
   



def to_decimal(oct_num):
    """
        >>> to_decimal(206)
        134
        >>> to_decimal(237) 
        159
        >>> to_decimal(35) 
        29
        >>> to_decimal(600) 
        384
        >>> to_decimal(420) 
        272
    """
    #- YOUR CODE STARTS HERE
    result = 0
    power = 0
    while oct_num > 0:
        digit = oct_num%10
        result += digit*(8**power)
        power += 1
        oct_num //= 10
    return result



def has_hoagie(num):
    """
        >>> has_hoagie(737) 
        True
        >>> has_hoagie(35) 
        False
        >>> has_hoagie(-6060) 
        True
        >>> has_hoagie(-111) 
        True
        >>> has_hoagie(6945) 
        False
        >>> has_hoagie(1060)
        True
        >>> has_hoagie(12345678666123456)
        True
    """
    #- YOUR CODE STARTS HERE
    
    num = abs(num)   
    while num > 100:
        digit_first = num%10
        digit_second = num//100%10
        if digit_first == digit_second:
            return True
        num//=10
    return False

def is_identical(num_1, num_2):
    """
        >>> is_identical(51111315, 51315)
        True
        >>> is_identical(7006600, 7706000)
        True
        >>> is_identical(135, 765) 
        False
        >>> is_identical(2023, 20) 
        False
    """
    #- YOUR CODE STARTS HERE
    power_1 = 0
    power_2 = 0
    while num_1 > 0  and num_2 > 0:
        digit_1 = num_1%10
        digit_2 = num_2%10
        if num_1//10%10 == digit_1:
            num_1//=10
            power_1+=1
        elif num_2//10%10 == digit_2:
            num_2//=10
            power_2+=1
        else:
            if power_1 == power_2 and digit_1 != digit_2:
                return False
            else:
                num_2//=10
                num_1//=10
                power_1+=1
                power_2+=1
                
    return True


def hailstone(num):
    """
        >>> hailstone(10)
        [10, 5, 16, 8, 4, 2, 1]
        >>> hailstone(1)
        [1]
        >>> hailstone(27)
        [27, 82, 41, 124, 62, 31, 94, 47, 142, 71, 214, 107, 322, 161, 484, 242, 121, 364, 182, 91, 274, 137, 412, 206, 103, 310, 155, 466, 233, 700, 350, 175, 526, 263, 790, 395, 1186, 593, 1780, 890, 445, 1336, 668, 334, 167, 502, 251, 754, 377, 1132, 566, 283, 850, 425, 1276, 638, 319, 958, 479, 1438, 719, 2158, 1079, 3238, 1619, 4858, 2429, 7288, 3644, 1822, 911, 2734, 1367, 4102, 2051, 6154, 3077, 9232, 4616, 2308, 1154, 577, 1732, 866, 433, 1300, 650, 325, 976, 488, 244, 122, 61, 184, 92, 46, 23, 70, 35, 106, 53, 160, 80, 40, 20, 10, 5, 16, 8, 4, 2, 1]
        >>> hailstone(7)
        [7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
        >>> hailstone(19)
        [19, 58, 29, 88, 44, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
    """
    #- YOUR CODE STARTS HERE
    result = []
    result.append(num)
    while num != 1:
        if num%2 == 0:
            result.append(num//2)
            num = num//2
        else:
            result.append(num*3+1)
            num = num*3+1
    return result



def overloaded_add(d, key, value):
    """
        Adds the key value pair to the dictionary. If the key is already in the dictionary, the value is made a list and the new value is appended to it.
        >>> d = {"Alice": "Engineer"}
        >>> overloaded_add(d, "Bob", "Manager")
        >>> overloaded_add(d, "Alice", "Sales")
        >>> d == {"Alice": ["Engineer", "Sales"], "Bob": "Manager"}
        True

        >>> d = {"Alice": "Engineer"}
        >>> overloaded_add(d, "Bob", "Manager")
        >>> overloaded_add(d, "Alice", "Sales")
        >>> overloaded_add(d, "Alice", "chicken watching")
        >>> overloaded_add(d, "Alice", "watch paint dry")
        >>> overloaded_add(d, "Bob", "watching alice")
        >>> d == {"Alice": ["Engineer", "Sales", "chicken watching", "watch paint dry"], "Bob": ["Manager", "watching alice"]}
        True
    """
    #- YOUR CODE STARTS HERE
    if key in d:
        if type(d[key]) == list:
            d[key].append(value)
        else:
            d[key] = [d[key]] + [value]
    else:
        d[key] =value


def by_department(d):
    """
        >>> employees = {
        ...    1: {'name': 'John Doe', 'position': 'Manager', 'department': 'Sales'},
        ...    2: {'position': 'Budget Advisor', 'name': 'Sara Miller', 'department': 'Finance'},
        ...    3: {'name': 'Jane Smith', 'position': 'Engineer', 'department': 'Engineering'},
        ...    4: {'name': 'Bob Johnson', 'department': 'Finance', 'position': 'Analyst'},
        ...    5: {'position': 'Senior Developer', 'department': 'Engineering', 'name': 'Clark Wayne'}
        ...    }

        >>> by_department(employees)
        {'Sales': [{'emp_id': 1, 'name': 'John Doe', 'position': 'Manager'}], 'Finance': [{'emp_id': 2, 'name': 'Sara Miller', 'position': 'Budget Advisor'}, {'emp_id': 4, 'name': 'Bob Johnson', 'position': 'Analyst'}], 'Engineering': [{'emp_id': 3, 'name': 'Jane Smith', 'position': 'Engineer'}, {'emp_id': 5, 'name': 'Clark Wayne', 'position': 'Senior Developer'}]}
    """
    #- YOUR CODE STARTS HERE
    new_d = {}
    for key,value in d.items():
        if value["department"] in new_d:
            new_d[value["department"]] += [{"emp_id":key,"name":d[key]["name"], "position":d[key]["position"]}]
        else:
            new_d[value["department"]] = [{"emp_id":key,"name":d[key]["name"], "position":d[key]["position"]}]
    return new_d


def successors(file_name):
    """
        >>> expected = {'.': ['We', 'Maybe'], 'We': ['came'], 'came': ['to'], 'to': ['learn', 'have', 'make'], 'learn': [',', 'how'], ',': ['eat'], 'eat': ['some'], 'some': ['pizza'], 'pizza': ['and', 'too'], 'and': ['to'], 'have': ['fun'], 'fun': ['.'], 'Maybe': ['to'], 'how': ['to'], 'make': ['pizza'], 'too': ['!']}
        >>> returnedDict = successors('items.txt')
        >>> expected == returnedDict
        True
        >>> returnedDict['.']
        ['We', 'Maybe']
        >>> returnedDict['to']
        ['learn', 'have', 'make']
        >>> returnedDict['fun']
        ['.']
        >>> returnedDict[',']
        ['eat']
    """
    file_path = get_path(file_name)
    with open(file_path, 'r') as file:   
        contents = file.read()  # You might change .read() for .readlines() if it suits your implementation better
        # --- YOU CODE STARTS HERE
        successor_d = {}
        items = ["."]
        i = 0
        while contents:
            if not contents[i].isalnum():
                if contents[i] != "\n":
                    items.append(contents[:i])
                if contents[i] != " " and contents[i] != "\n":
                    items.append(contents[i])
                contents = contents[i+1:]
                i = 0
            else:
                i += 1

        for i in range(len(items)-1):
            if items[i] in successor_d:
                if not items[i+1] in successor_d[items[i]]:
                    successor_d[items[i]].append(items[i+1])
            else: 
                successor_d[items[i]] = [items[i+1]]
        return successor_d

def addToTrie(trie, word):
    """
        The following dictionary represents the trie of the words "A", "I", "Apple":
            {'a' : {'word' : True, 'p' : {'p' : {'l' : {'e' : {'word' : True}}}}, 'i' : {'word' : True}}}}
       
        >>> trie_dict = {'a' : {'word' : True, 'p' : {'p' : {'l' : {'e' : {'word' : True}}}}, 'i' : {'word' : True}}} 
        >>> addToTrie(trie_dict, 'art')
        >>> trie_dict
        {'a': {'word': True, 'p': {'p': {'l': {'e': {'word': True}}}}, 'i': {'word': True}, 'r': {'t': {'word': True}}}}
        >>> addToTrie(trie_dict, 'moon') 
        >>> trie_dict
        {'a': {'word': True, 'p': {'p': {'l': {'e': {'word': True}}}}, 'i': {'word': True}, 'r': {'t': {'word': True}}}, 'm': {'o': {'o': {'n': {'word': True}}}}}
    """
    #- YOUR CODE STARTS HERE
    if len(word)==1:
        trie[word[0]] = {"word":True}
    else:
        if not word[0] in trie:
            trie[word[0]] = {}
            return addToTrie(trie[word[0]],word[1:])
        else:
            return addToTrie(trie[word[0]],word[1:])
        

def createDictionaryTrie(file_name):
    """        
        >>> trie = createDictionaryTrie("words.txt")
        >>> trie == {'b': {'a': {'l': {'l': {'word': True}}, 't': {'s': {'word': True}}}, 'i': {'r': {'d': {'word': True}},\
                     'n': {'word': True}}, 'o': {'y': {'word': True}}}, 't': {'o': {'y': {'s': {'word': True}}},\
                     'r': {'e': {'a': {'t': {'word': True}}, 'e': {'word': True}}}}}
        True
    """
    file_path = get_path(file_name)
    with open(file_path, 'r') as file:   
        contents = file.read()  # You might change .read() for .readlines() if it suits your implementation better 
        #- YOUR CODE STARTS HERE
        contents = contents.split()
        trie = {}
        for word in contents:
            addToTrie(trie,word)
    return trie



def wordExists(trie, word):
    """
        >>> trie_dict = {'a' : {'word' : True, 'p' : {'p' : {'l' : {'e' : {'word' : True}}}}, 'i' : {'word' : True}}} 
        >>> wordExists(trie_dict, 'armor')
        False
        >>> wordExists(trie_dict, 'apple')
        True
        >>> wordExists(trie_dict, 'apples')
        False
        >>> wordExists(trie_dict, 'a')
        True
        >>> wordExists(trie_dict, 'as')
        False
        >>> wordExists(trie_dict, 'tt')
        False
    """
    #- YOUR CODE STARTS HERE
    if len(word)==0:
        if trie["word"]:
            return True
        return False
    else:
        if word[0] in trie:
            return True and wordExists(trie[word[0]],word[1:])
        return False and wordExists(trie[word[0]],word[1:])  




def run_tests():
    import doctest
    # Run start tests in all docstrings
    #doctest.testmod(verbose=True)
    
    # Run start tests per function - Uncomment the next line to run doctest by function. Replace rectangle with the name of the function you want to test
    doctest.run_docstring_examples(overloaded_add, globals(), name='HW1',verbose=True)   

if __name__ == "__main__":
    run_tests()
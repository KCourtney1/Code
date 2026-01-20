# LAB1
# REMINDER: The work in this assignment must be your own original work and must be completed alone

def frequency(txt):
    '''
        preconditions:  txt is an non-empty string
        postconditions: returns the frequency of ever char in txt string
        >>> frequency('mama')
        {'m': 2, 'a': 2}
        >>> answer = frequency('We ARE Penn State!!!')
        >>> answer
        {'w': 1, 'e': 4, 'a': 2, 'r': 1, 'p': 1, 'n': 2, 's': 1, 't': 2}
        >>> frequency('One who IS being Trained')
        {'o': 2, 'n': 3, 'e': 3, 'w': 1, 'h': 1, 'i': 3, 's': 1, 'b': 1, 'g': 1, 't': 1, 'r': 1, 'a': 1, 'd': 1}
    '''
    # - YOUR CODE STARTS HERE -
    frequency_dic = {}
    for char in txt:
        if char.isalpha():
            char = char.lower()
            if char in frequency_dic:
                frequency_dic[char] += 1
            else:
                frequency_dic[char] = 1
    return frequency_dic

def invert(d):
    """
        preconditions: d is an non-empty dict
        postconditions: returns a dict of d inverted, key:value to value:key
        >>> invert({'one':1, 'two':2,  'three':3, 'four':4})
        {1: 'one', 2: 'two', 3: 'three', 4: 'four'}
        >>> invert({'one':1, 'two':2, 'uno':1, 'dos':2, 'three':3})
        {3: 'three'}
        >>> invert({'123-456-78':'Sara', '987-12-585':'Alex', '258715':'sara', '00000':'Alex'}) 
        {'Sara': '123-456-78', 'sara': '258715'}
    """
    # - YOUR CODE STARTS HERE -
    invert_d = {}
    for key , Value in d.items():
        count = 0
        for _ , Value2 in d.items():
            if Value2 == Value:
                count += 1
        if count == 1:
            invert_d[Value] = key
    return invert_d

def employee_update(d, bonus, year):
    """
        precondition: d is an non-empty dict of dict, bonus is a float or int, year is and int
        postcondition: Returns dict -> adds the key:value pair with bonus applied
        >>> records = {2020:{"John":["Managing Director","Full-time",65000],"Sally":["HR Director","Full-time",60000],"Max":["Sales Associate","Part-time",20000]}, 2021:{"John":["Managing Director","Full-time",70000],"Sally":["HR Director","Full-time",65000],"Max":["Sales Associate","Part-time",25000]}}
        >>> employee_update(records,7500,2022)
        {2020: {'John': ['Managing Director', 'Full-time', 65000], 'Sally': ['HR Director', 'Full-time', 60000], 'Max': ['Sales Associate', 'Part-time', 20000]}, 2021: {'John': ['Managing Director', 'Full-time', 70000], 'Sally': ['HR Director', 'Full-time', 65000], 'Max': ['Sales Associate', 'Part-time', 25000]}, 2022: {'John': ['Managing Director', 'Full-time', 77500], 'Sally': ['HR Director', 'Full-time', 72500], 'Max': ['Sales Associate', 'Part-time', 32500]}}
    """
    # - YOUR CODE STARTS HERE -
    updated_year = {}
    for employee,status in d[year-1].items():   #goes through dict in the pervious year from year given
        updated_employee = status[0:2] 
        updated_employee.append(status[-1]+bonus)
        updated_year[employee] = updated_employee   #adds employee and their status to the updated year
    d[year] = updated_year
    return d

def run_tests():
    import doctest

    # Run start tests in all docstrings
    #doctest.testmod(verbose=True)
    
    # Run start tests per function - Uncomment the next line to run doctest by function. Replace frequency with the name of the function you want to test
    doctest.run_docstring_examples(employee_update, globals(), name='LAB1',verbose=True)   

if __name__ == "__main__":
    run_tests()


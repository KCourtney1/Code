
def remove_punctuation(text):
    assert type(text) == str
    result = ""
    for char in text:
        if char.isalpha() or char == " ":
            result += char
        else:
            result += " "
    return result

def remove_punctuation_v2(text):
    assert type(text) == str
    result = list(text)
    for i in range(len(result)):
        char = result[i]
        if not(char.isalpha()) or char != " ":
            result[i] = " "
    return "".join(result)

def is_alpha(s):
    assert type(s) == str
    for char in s:
        value = ord(char)
        if value < 65 or value > 122 or 91<value<97:
            return False
    return True

def is_lower(s): 
    assert type(s) == str
    for char in s:
        value = ord(char)
        if value <97 or value > 122:
            return False
    return True

def lower(s): 
    assert type(s) == str
    result = '' #result = list(s)
    for char in s: #for i in range(len(result)): #char = result[i]
        if is_alpha(char) and not is_lower(char):
            value = ord(char)
            new_char = chr(value+32)
            result += new_char #result[i]= new_char
        else:               #removed
            result += char   #removed   
    return result #return "".join(result)

def strip(s):
    assert type(s) == str
    start = 0
    size = len(s)
    end = size-1

    while start < size and s[start] == " ":
        start+= 1
    
    while end > 0 and s[end]==" ":
        end -=1

    if start == size and end == 0:
        return s
    return s[start:end+1]
    
    result = ""
    for i in range(start,end+1):
        result += s[i]
    return result

def is_start(s, substr):
    sub_size = len(substr)
    size = len(s)
    if size >= sub_size:
        return substr == s[:sub_size]
        # if substr == s[:sub_size]:
        #     return True
        # else:
        #     return False
    else: 
        return False
    
def my_in(lst,value):
    assert type(lst) == list
    for item in lst:
        if item == value:
            return True
    return False

def my_index(lst,value):
    assert type(lst) == list
    for i in range(len(lst)):
        if lst[i] == value:
            return i
    return -1

def swap(lst,h,k):
    assert type(lst) == list
    temp = lst[h]
    lst[h] = lst[k]
    lst[k] = temp

def reverse_d(lst):
    assert type(lst) == list
    size = len(lst)
    i = 0
    j = -1
    while i < size//2:
        swap(lst,i,j)
        i-=1
        j-=1

def reverse_d_v2(lst):
    assert type(lst) == list
    size = len(lst)
    i = size-1
    while i >= 0:
        value = lst[i]
        del lst[i]
        lst.append(value)
        i-=1


def reverse_non_d(lst):
    assert type(lst) == list
    new_lst = []
    for i in range(len(lst)-1,-1,-1):
        new_lst.append(lst[i])
        #new_lst = new_lst + [lst[i]] #new_lst += lst[i]

    
#all num
def all_num(s):
    assert type(s) == str
    for char in s:
        value = ord(char)
        if value >= 49 and value <= 57:
            return True
    return False

#is_upper
def is_upper(s): 
    assert type(s) == str
    for char in s:
        value = ord(char)
        if value >=65 and value <= 90:
            return True
    return False

#upper
def upper(s): 
    assert type(s) == str
    result = '' #result = list(s)
    for char in s: #for i in range(len(result)): #char = result[i]
        if is_alpha(char) and not is_upper(char):
            value = ord(char)
            new_char = chr(value-32)
            result += new_char #result[i]= new_char
        else:               #removed
            result += char   #removed   
    return result #return "".join(result)

#ends_with
def ends_with(s, substr):
    sub_size = len(substr)
    size = len(s)
    if size >= sub_size:
        return substr == s[-sub_size:]
        # if substr == s[:sub_size]:
        #     return True
        # else:
        #     return False
    else: 
        return False
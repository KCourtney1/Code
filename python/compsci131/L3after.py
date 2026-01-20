
def get_tip(bill, tip_p):
    """precondition: bill is a postive number and tip_p is a value between 0 and 100
    prostcondition: returns an float of how much to tip"""
    tip = bill*(tip_p/100)
    if tip >2:
        return round(tip,2)
    else:
        return 2.0
    
def check_num(n):
    """precondition: n is a numerical value
    postcondition: returns string based on if a number is pos or neg or if 0 zero"""
    if n < 0:
        return "Negative"
    elif n > 0:
        return "Positive"
    return "Zero"

def get_sum(n):
    """precondition: n is a positive number
    postcondition: returns sum of 1 + 1/2 + 1/3 + 1/4 + ... + 1/n to five decimal places"""
    sum = 1
    for x in range(2,n+1):
        sum = sum + (1/x)
    return round(sum,5)

def get_sqrt(n, iterations):
    """precondition: n is a positive number and iterations is a positive number
    postcondition: return a positve float represinting an aproximation of sqrt"""
    sqrt = n/2
    for x in range(1,iterations+1):
        sqrt = 1/2*(sqrt+(n/sqrt))
    return sqrt
import math
import pandas as pd

def f(x):
    return math.exp(math.sin(x))
    
def f_prime(x):
    return math.cos(x)*math.exp(math.sin(x))

def f_expo(x):
    return math.exp((2*x) + 1)

def f_primeExpo(x):
    return 2*math.exp((2*x) + 1)

def FD(a, h):
    return (f(a+h) - f(a))/h

def BD(a, h):
    return (f(a) - f(a-h))/h

def CD(a, h):
    return (f(a+h) - f(a-h))/(2*h)

def CD_expo(a, h):
    return (f_expo(a+h) - f_expo(a-h))/(2*h)

def threePointDiff(a, h):
    return ((-3*f_expo(a)) + (4*f_expo(a+h)) - f_expo(a+(2*h)))/(2*h)

def threePointDiffEnd(a, h):
    return ((3*f_expo(a)) - (4*f_expo(a-h)) + f_expo(a-(2*h)))/(2*h)

def create_table_FBCdiff(a, h, start, b):
    rows = []
    AvgError = 0
    while a <= b:
        if a == start:
            Error = abs(f_prime(a) - FD(a,h))
            approx = FD(a, h)
        elif a+h >= b:
            Error = abs(f_prime(a) - BD(a,h))
            approx = BD(a, h)
        else:
            Error = abs(f_prime(a) - CD(a,h))
            approx = CD(a, h)
        rows.append([a, f_prime(a), approx, Error])
        AvgError += Error
        a += h
    table = pd.DataFrame(rows, columns=["a", "actual", "Approx. Value", "Error"])
    return [h, table, AvgError*h]

def create_table_3point(a, h, start, b):
    rows = []
    AvgError = 0
    while a <= b:
        if a >= b-h:
            Error = abs(f_primeExpo(a) - threePointDiffEnd(a,h))
            approx = threePointDiffEnd(a, h)
        else:
            Error = abs(f_primeExpo(a) - threePointDiff(a,h))
            approx = threePointDiff(a, h)
        rows.append([a, f_primeExpo(a), approx, Error])
        AvgError += Error
        a += h
    table = pd.DataFrame(rows, columns=["a", "actual", "Approx. Value", "Error"])
    return [h, table, AvgError*h]

def power_Tables(a, h, i, j):
    powerTables = []
    while i <= j:
        powerTables.append(create_table_3point(a, h**i, 0, 1))
        i+=1
    return powerTables

for table in power_Tables(0, .1, 1, 1):
    print("h =", table[0])
    print(table[1])
    print("Avg-Error", table[2],"\n")
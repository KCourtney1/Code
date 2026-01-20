import math
import pandas as pd

def f(x):
    return math.exp(math.sin(x))
    
def f_prime(x):
    return math.cos(x)*math.exp(math.sin(x))

def FD(a, h, stop):
    interval = []
    while a <= stop:
        interval.append((f(a+h) - f(a))/h)
        a += h
    return interval

def BD(a, h, stop):
    interval = []
    while a <= stop:
        interval.append((f(a) - f(a-h))/h)
        a += h
    return interval

def CD(a, h, stop):
    interval = []
    while a <= stop:
        interval.append((f(a+h) - f(a-h))/(2*h))
        a += h
    return interval

def FD_AvgError(a, h, stop):
    total = 0
    while a <= stop-h:
        total += abs(f_prime(a) - ((f(a+h) - f(a))/h))
        a += h
    return total * h
    
def BD_AvgError(a, h, stop):
    total = 0
    a += h
    while a <= stop:
        total += abs(f_prime(a) - ((f(a) - f(a-h))/h))
        a += h
    return total * h
    
def CD_AvgError(a, h, stop):
    total = 0
    a += h
    while a <= stop-h:
        total += abs(f_prime(a) - ((f(a+h) - f(a-h))/(2*h)))
        a += h
    return total * h


def create_tables(a, h, i, stop):
    FDrows = []
    BDrows = []
    CDrows = [] 
    while i <= stop:
        FDAvgError = FD_AvgError(a, h**i, math.pi/2)
        BDAvgError = BD_AvgError(a, h**i, math.pi/2)
        CDAvgError = CD_AvgError(a, h**i, math.pi/2)
        FDrows.append([h**i, f_prime(a), FD(a, h**i, math.pi/2), FDAvgError])
        BDrows.append([h**i, f_prime(a), BD(a, h**i, math.pi/2), BDAvgError])
        CDrows.append([h**i, f_prime(a), CD(a, h**i, math.pi/2), CDAvgError])

        i+=1
    FDtable = pd.DataFrame(FDrows, columns=["h", "actual", "FD", "AvgError"])
    BDtable = pd.DataFrame(BDrows, columns=["h", "actual", "BD", "AvgError"])
    CDtable = pd.DataFrame(CDrows, columns=["h", "actual", "CD", "AvgError"])
    return [FDtable, BDtable, CDtable]

for table in create_tables(0, 1/2, 3, 4):
    print(table)
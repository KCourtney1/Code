import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def f(x,y):
    return x**2 - (3*x*y) + 2*(y**3)

def fx(x, y, h):
    return (f(x+h, y) - f(x, y))/h

def fy(x, y, h):
    return (f(x, y+h) - f(x , y))/h

hls = {.5,.1,.05}

print("x")
for h in hls:
    print(fx(1,-1, h))

print("y")
for h in hls:
    print(fy(1,-1, h))

print(f(1,-1))
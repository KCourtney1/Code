import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def ordDiffre1(a ,b , dt, y0):
    def f(r,s):
        return 1/r**2-s/r-s**2
    
    actual = -1/a
    if math.isclose(a,b):
        return [[a, y0, actual, abs(actual-y0)]]
    else:
        return [[a, y0, actual, abs(actual-y0)]] + ordDiffre1(a+dt, b, dt, y0+dt*f(a,y0))
    
def ordDiffre2(a ,b , dt, y0):
    def f(r,s):
        return (1/r)*(2-s)
    
    actual = 2/a+2
    if math.isclose(a,b):
        return [[a, y0, actual, abs(actual-y0)]]
    else:
        return [[a, y0, actual, abs(actual-y0)]] + ordDiffre2(a+dt, b, dt, y0+dt*f(a,y0))

def ordinarydiff1():
    T=2

    t0=1
    dt=0.2
    n=int((T-t0)/dt)
    y0=-1
    def f(r,s):
        return 1/r**2-s/r-s**2

    time=[t0+i*dt for i in range(n+1)]
    y=[y0 for i in range(n+1)]
    for j in range(n):
        y[j+1]=y[j]+dt*f(time[j],y[j])

    for i in range(n+1):
        print(time[i], y[i])

def ordinarydiff2():
    T = 3
    t0 = 2
    dt = 0.1

    n = int((T-t0)/dt)
    y0 = 3

    def f(tj,yj):
        return (1/tj)*(2-yj)

    time = [t0+i*dt for i in range(n+1)]
    y = [y0 for i in range(n+1)]

    for j in range(n):
        y[j+1]=y[j]+dt*f(time[j],y[j])

    for i in range(n+1):
        print(time[i], y[i])
    # return time,y

dtValues = [.2,.1,.05,.0125,.00625]
plots = {}
for dt in dtValues:
    table = pd.DataFrame(ordDiffre1(1, 2, dt, -1),columns=["time", "Approx. Value", "actual", "error"])
    time = table["time"].tolist()
    approx = table["Approx. Value"].tolist()
    actual = table["actual"].tolist()
    error = table["error"].tolist()
    plots["Approx. dt = " + str(dt)] = plt.plot(time, approx)
plots["Actual Value"] = plt.plot(time, approx)

plt.legend(plots)
plt.title("Time vs Value")
plt.xlabel("Time")
plt.ylabel("Value")
plt.show()
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def f(x, t):
    return (x**2) * (math.e**t)

#Calculate the partial derivatives f_x and f_t as functions of x and t.
def fx(x,t):
    return (2*x) * (math.e**t)

def ft(x,t):
    return ((x)**2) * (math.e**t)

#Approximate the partial derivatives f_x (-1,1) and f_t (-1,1)
def approx_fx(x, t, h):
    return (f(x+h, t) - f(x, t))/h

def approx_ft(x, t, h):
    return (f(x, t+h) - f(x, t))/h

rows_x = []
rows_t = []
hValues = [.1, .01, .001, .0001]

#Calculate the errors in the partial derivative approximations of f_x (-1,1) and f_t (-1,1) for the above h values.
#outputs in the console
for h in hValues:
    actual_x = fx(-1,1)
    approx_x = approx_fx(-1, 1, h)

    actual_t = ft(-1,1)
    approx_t = approx_ft(-1, 1, h)

    row_x = [h, approx_x, actual_x, (abs(approx_x - actual_x))]
    row_t = [h, approx_t, actual_t, (abs(approx_t - actual_t))]
    rows_x.append(row_x)
    rows_t.append(row_t)

#Find the values of f_x (-1,1) and f_t (-1,1).
print("f_x(-1, 1) = x^2*e^t = {}".format(fx(-1,1)))
print("f_t(-1, 1) = 2x*e^t = {}".format(ft(-1,1)))

table_x = pd.DataFrame(rows_x, columns=["h-value", "Approx. Value", "actual value", "error"])
table_t = pd.DataFrame(rows_t, columns=["h-value", "Approx. Value", "actual value", "error"])
print("fx:\n{}".format(table_x))
print("ft:\n{}".format(table_t)) 

#Plot f(x,1) on the interval of [-2, 2] and Plot f(-1,t) on the interval of [-1, 3].
valueLS_X = []
posLS_X = []
for x in np.linspace(-2,2,200):
    posLS_X.append(x)
    valueLS_X.append(f(x, 1))
valueLS_T = []
posLS_T = []
for t in np.linspace(-1,4,200):
    posLS_T.append(t)
    valueLS_T.append(f(-1, t))

figure, axis = plt.subplots(1, 2)
axis[0].plot(posLS_X, valueLS_X)
axis[0].set_title("f(x, 1) [-2, 2]")

axis[1].plot(posLS_T, valueLS_T)
axis[1].set_title("f(-1, t) [-1, 3]")
figure.supxlabel("x")
figure.supylabel("value")
plt.show()
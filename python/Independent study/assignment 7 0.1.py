import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# set ranges and deltas
dx = .1
dt = .1
x_range = np.linspace(-2, 2, (int(1/dx)))
t_range = np.linspace(-1, 3, (int(1/dt)))

def f(x,t):
    return (x**2) * (math.e**t)

#get density table by loop x nested loop y with row format x pos, y pos, density at (x, y)
def get_density_table(x_range, t_range):
    rows = []
    for x in x_range:
        for t in t_range:
            density = f(x, t)
            row = [x, t, density]
            rows.append(row)
    density_table = pd.DataFrame(rows, columns=["x", "t", "density"])
    return density_table

#intit varibles for ploting
table = get_density_table(x_range, t_range)
X = table["x"].tolist()
T = table["t"].tolist()
Z = table["density"].tolist()

#creates a figure with an 3d plot 
fig = plt.figure(figsize=(10, 8))
ax = plt.axes(projection='3d')
ax.plot_trisurf(X, T, Z, linewidth=0, antialiased=False, cmap = "hot")

ax.set_xlabel('x', fontsize=12)
ax.set_ylabel('t', fontsize=12)
ax.set_zlabel('density', fontsize=12)
ax.set_title('density for f(x, t) = x^2e^t; dt = {}'.format(dt))
plt.show()
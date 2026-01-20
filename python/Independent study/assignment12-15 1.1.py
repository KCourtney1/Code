import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import time

class Exact:
    def __init__(self, dx, BC, IC, x_s, gamma, epsilon) -> None:
        self.epsilon = epsilon
        self.gamma = gamma
        self.dx = dx
        self.BC = BC
        self.IC = IC
        self.x_s = x_s

    def __str__(self):
        return "Exact"

    @property
    def dx(self):
        return self._dx
    
    @dx.setter
    def dx(self, dx):
        self._dx = dx
        self.dt = (1/(1+self.epsilon)) * (0.8 * ((2 - self.gamma) / (2 + self.gamma)) * self.dx) #0.8 * ((2 - self.gamma) / (2 + self.gamma)) * self.dx
        self.M = int(1/self.dx) + 1
        self.N = int(1/self.dt) + 1
        self.p = np.zeros((self.N, self.M))
    
    def get_vbar(self, x):
        if x <= self.x_s:
            return 1
        else:
            return 1 + self.epsilon

    def update_p(self):
        for n in range(self.N):
            for j in range(self.M):
                t = n * self.dt
                x = j * self.dx
                if ((0 <= x <= self.x_s) and (x > t)) or ((self.x_s <= x <= 1) and (t<=(1/(1+self.epsilon)*(x-self.x_s)+self.x_s))):
                    self.p[n,j] = self.IC
                else:
                    self.p[n,j] = self.BC

class Upwind(Exact):
    def __init__(self, dx, BC, IC, x_s, gamma, epsilon) -> None:
        super().__init__(dx, BC, IC, x_s, gamma, epsilon)  

    def __str__(self):
        return "Upwind"

    def update_p(self):
        self.p[:, 0] = self.BC                                                               #set matrix boundary condition
        self.p[0, 1:] = self.IC                                                                #set matrix initial condition
        for n in range(self.N - 1):
            for j in range(1, self.M):
                nu = self.get_vbar(j*self.dx) * (self.dt / self.dx)
                self.p[n+1, j] = (1 - nu) * self.p[n, j] + nu * self.p[n, j-1]              #set density at point P[n+1][j];  p[n+1, j] = (1 - nu) * p[n, j] + nu * p[n, j-1]

class FilteredUpwind(Exact):
    def __init__(self, dx, BC, IC, x_s, gamma, epsilon) -> None:
        super().__init__(dx, BC, IC, x_s, gamma, epsilon)

    def __str__(self):
        return "Filtered Upwind"

    def update_p(self):
        self.p[:, 0] = self.BC    #set matrix boundary condition
        self.p[0, 1:] = self.IC   #set matrix initial condition

        for j in range(1, self.M):
            nu = self.get_vbar(j*dx) * (self.dt/self.dx)
            self.p[1, j] = (1 - nu) * self.p[1, j] + nu * self.p[1, j-1]

        for n in range(self.N - 1):
            for j in range(1, self.M):
                nu = self.get_vbar(j*dx) * (self.dt/self.dx)
                self.p[n + 1, j] = (self.gamma + (1 - nu) * (1 - (self.gamma / 2))) * self.p[n, j] \
                                    - (self.gamma / 2) * self.p[n - 1, j] \
                                    + nu * (1 - (self.gamma / 2)) * self.p[n, j - 1]

def plot_sol(S, ax, title):
    x = np.linspace(0, 1, (S.M))
    t = np.linspace(0, 1, (S.N))
    X, T = np.meshgrid(x, t)

    ax.plot_surface(X, T, S.p, cmap='viridis', edgecolor='none', alpha=0.8)    #colors = plasma, hot, jet, summer, copper
    ax.set_xlabel('x', fontsize=12);    ax.set_ylabel('t', fontsize=12);    ax.set_zlabel('density', fontsize=12);    ax.set_title(title)

def rate_of_convergence(error_table):# epsilon = 0, .5 t = 1
    rates = []
    for i in range(1, len(error_table)):
        dx1 = error_table.iloc[i-1, 0]       #second is position in the table
        dx2 = error_table.iloc[i, 0]
        error1 = error_table.iloc[i-1, -1]   #i, use t = 1 and then change gamma
        error2 = error_table.iloc[i, -1]     #i + 1
        rate = np.log(error1 / error2) / np.log(dx1 / dx2)
        rates.append(rate)
    return rates

def error(approx, exact, tvalues = [0, .2, .4, .6, .8, 1]):
    tval_errors = []
    for t_val in tvalues:
        n = int(t_val/exact.dx)
        error = np.abs(approx.p[n, :] - exact.p[n, :])
        tval_errors.append(np.sum(error)*exact.dx)
    return tval_errors

def get_xslice(p, x):   #x is index between 0 and M
    return  p[:, x]

def get_tslice(p, t):   #t is index between 0 and M
    return p[t, :]

start_time = time.time()
BC = .47
IC = 0.0
x_s = .5
gamma_values = [0, 1.75]
epsilon_values = [0.5]

filtered_error_dataframes = []
t_1_errors = {}
dx_UW_error, dx_FUW_error = [],[]
for epsilon in epsilon_values:
    for gamma in gamma_values:
        for i in range(5, 7):
            dx = (2)**(-i)

            plots = [Upwind_s, filterUpwind_s, Exact_s] = Upwind(dx, BC, IC, x_s, gamma, epsilon), FilteredUpwind(dx, BC, IC, x_s, gamma, epsilon), Exact(dx, BC, IC, x_s, gamma, epsilon)
            Upwind_s.update_p(); filterUpwind_s.update_p(); Exact_s.update_p()
            dx_UW_error.append([dx] + error(Upwind_s, Exact_s))
            dx_FUW_error.append([dx] + error(filterUpwind_s, Exact_s))

        error_UW_table = pd.DataFrame(dx_UW_error, columns=["dx","t=0", "t=0.2", "t=0.4", "t=0.6", "t=0.8", "t=1.0"])       
        #error_UW_table.to_csv("upwindErrorTable Epsilon={}, Gamma = {}.csv".format(epsilon, gamma))                                                                                          

        error_FUW_table = pd.DataFrame(dx_FUW_error, columns=["dx", "t=0", "t=0.2", "t=0.4", "t=0.6", "t=0.8", "t=1.0"])
        #error_FUW_table.to_csv("FilteredUpwindErrorTable Epsilon={}, Gamma = {}.csv".format(epsilon, gamma))
        filtered_error_dataframes.append(error_FUW_table)
        dx_UW_error, dx_FUW_error = [],[]

        t_1_errors["gamma = {}".format(gamma)] = error_FUW_table["t=1.0"].values
        for df in filtered_error_dataframes:
            roc = rate_of_convergence(df)
            roc_df = pd.DataFrame(roc, columns=["error"])
            #roc_df.to_csv("Filtered ROC for epsilon = {}, gamma = {}.csv".format(epsilon, gamma))
        filtered_error_dataframes = []

end_time = time.time()
print("Execution time: {:.2f} seconds".format(end_time - start_time))                                              

#figure 1
def draw_next(event):
    global GraphIndex
    GraphIndex = (GraphIndex + 1) % len(plots)
    ax1.clear()
    plot_sol(plots[GraphIndex], ax1, '{} at dx = {}; dt = {};'.format(str(plots[GraphIndex]), plots[GraphIndex].dx, plots[GraphIndex].dt))
    plt.draw()

def draw_prev(event):
    global GraphIndex
    GraphIndex = (GraphIndex - 1) % len(plots)
    ax1.clear()
    plot_sol(plots[GraphIndex], ax1, '{} at dx = {}; dt = {};'.format(str(plots[GraphIndex]), plots[GraphIndex].dx, plots[GraphIndex].dt))
    plt.draw()

#figure 1
GraphIndex = 0
fig1 = plt.figure(figsize=plt.figaspect(.7))
ax1 = fig1.add_subplot(111, projection='3d')
plot_sol(plots[0], ax1, '{} at dx = {}; dt = {}'.format(str(plots[0]), plots[0].dx, plots[GraphIndex].dt))
button_next = Button(plt.axes([0.85, 0.01, 0.1, 0.05]), 'Next');        button_next.on_clicked(draw_next)
button_prev = Button(plt.axes([0.05, 0.01, 0.1, 0.05]), 'Previous');    button_prev.on_clicked(draw_prev)

#figure 2
fig2 = plt.figure(figsize=plt.figaspect(0.5))
f2_ax1 = fig2.add_subplot(121)
f2_ax2 = fig2.add_subplot(122)
f2_ax1.set_xlabel('dx', fontsize=12); f2_ax1.set_ylabel('error', fontsize=12)
f2_ax2.set_xlabel('ln(dx)', fontsize=12); f2_ax2.set_ylabel('ln(error)', fontsize=12)

for key, value in t_1_errors.items():
    dx = error_FUW_table["dx"].tolist()
    t_1 = value
    f2_ax1.plot(dx, t_1, 'o-', label=key)
    f2_ax2.plot(np.log(dx), np.log(t_1), 'o-', label=key)
f2_ax1.legend(); f2_ax2.legend()

#figure 3
fig3 = plt.figure(figsize=plt.figaspect(0.5))
f3_ax1 = fig3.add_subplot(1, 2, 1)
xplots = {"Upwind" : f3_ax1.plot(np.linspace(0, 1, (Upwind_s.N)), get_xslice(Upwind_s.p, Upwind_s.M//2 + 1))
          ,"Filtered Upwind" : f3_ax1.plot(np.linspace(0, 1, (filterUpwind_s.N)), get_xslice(filterUpwind_s.p, filterUpwind_s.M//2 + 1))
            ,"Exact" : f3_ax1.plot(np.linspace(0, 1, (Exact_s.N)), get_xslice(Exact_s.p, Exact_s.M//2 + 1))}
plt.legend(xplots);     f3_ax1.set_xlabel('t', fontsize=12);    f3_ax1.set_ylabel('denisity', fontsize=12);     f3_ax1.set_title('slice at t')

f3_ax2 = fig3.add_subplot(1, 2, 2)
tplots = {"Upwind" : f3_ax2.plot(np.linspace(0, 1, (Upwind_s.M)), get_tslice(Upwind_s.p, Upwind_s.N//2 + 1))
          ,"Filtered Upwind" : f3_ax2.plot(np.linspace(0, 1, (filterUpwind_s.M)), get_tslice(filterUpwind_s.p, filterUpwind_s.N//2 + 1))
            ,"Exact" : f3_ax2.plot(np.linspace(0, 1, (Exact_s.M)), get_tslice(Exact_s.p, Exact_s.N//2 + 1))}
plt.legend(tplots);     f3_ax2.set_xlabel('x', fontsize=12);    f3_ax2.set_ylabel('denisity', fontsize=12);    f3_ax2.set_title('slice at x')

plt.show()
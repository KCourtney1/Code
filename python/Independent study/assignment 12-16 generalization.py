import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Exact:
    def __init__(self, dx, BC, IC, x_s, gamma, epsilon) -> None:
        self.epsilon = epsilon
        self.gamma = gamma
        self.dx = dx
        self.BC = BC
        self.IC = IC
        self.x_s = x_s

    @property
    def dx(self):
        return self._dx

    @dx.setter
    def dx(self, dx):
        self._dx = dx
        self.dt = (1/(epsilon+1)) * (0.8 * ((2 - self.gamma) / (2 + self.gamma)) * self.dx)
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

    def update_p(self):
        self.p[:, 0] = self.BC                                                               #set matrix boundary condition
        self.p[0, :] = self.IC                                                               #set matrix initial condition
        for n in range(self.N - 1):
            for j in range(1, self.M):
                nu = self.get_vbar(j*self.dx) * (self.dt / self.dx)
                self.p[n+1, j] = (1 - nu) * self.p[n, j] + nu * self.p[n, j-1]              #set density at point P[n+1][j];  p[n+1, j] = (1 - nu) * p[n, j] + nu * p[n, j-1]

class FilteredUpwind(Exact):
    def __init__(self, dx, BC, IC, x_s, gamma, epsilon) -> None:
        super().__init__(dx, BC, IC, x_s, gamma, epsilon)

    def update_p(self):
        self.p[:, 0] = BC
        self.p[0, :] = IC

        for n in range(1, self.N - 1):
            for j in range(1, self.M):
                nu = self.get_vbar(j*dx) * (self.dt/self.dx)
                if n == 1:
                    self.p[n, j] = (1 - nu) * self.p[n, j] + nu * self.p[n, j-1]
                else:
                    self.p[n + 1, j] = (self.gamma + (1 - nu) * (1 - (self.gamma / 2))) * self.p[n, j] \
                                                            - (self.gamma / 2) * self.p[n - 1, j] \
                                                            + nu * (1 - (self.gamma / 2)) * self.p[n, j - 1]

def plot_sol(S, ax, title):
    x = np.linspace(0, 1, (S.M))
    t = np.linspace(0, 1, (S.N))
    X, T = np.meshgrid(x, t)

    ax.plot_surface(X, T, S.p, cmap='copper', edgecolor='none', alpha=0.8)    #colors = plasma, hot, jet, summer, copper
    ax.set_xlabel('x', fontsize=12);    ax.set_ylabel('t', fontsize=12);    ax.set_zlabel('density', fontsize=12);    ax.set_title(title)

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

dx_UW_error, dx_FUW_error = [],[]
for i in range(5,12):
    dx = (2)**(-i)
    BC = .47
    IC = 0.0

    epsilon = 0.25                  # 0.0 <= epsilon <= 0.5
    gamma = 0
    x_s = 0.5

    Upwind_s, filterUpwind_s, Exact_s = Upwind(dx, BC, IC, x_s, gamma, epsilon), FilteredUpwind(dx, BC, IC, x_s, gamma, epsilon), Exact(dx, BC, IC, x_s, gamma, epsilon)
    Upwind_s.update_p(); filterUpwind_s.update_p(); Exact_s.update_p()
    dx_UW_error.append([dx] + error(Upwind_s, Exact_s))
    dx_FUW_error.append([dx] + error(filterUpwind_s, Exact_s))

error_UW_table = pd.DataFrame(dx_UW_error, columns=["dx","t=0", "t=.2", "t=.4", "t=.6", "t=.8", "t=1"])       
error_UW_table.to_excel("upwindErrorTable.xlsx")                                                                                           

error_FUW_table = pd.DataFrame(dx_FUW_error, columns=["dx","t=0", "t=.2", "t=.4", "t=.6", "t=.8", "t=1"])
error_FUW_table.to_excel("FilteredUpwindErrorTable.xlsx")                                                 

#figure 1
fig1 = plt.figure(figsize=plt.figaspect(0.5))                                                       
f1_ax1 = fig1.add_subplot(1,3,1, projection='3d')                                                   
f1_ax2 = fig1.add_subplot(1,3,2, projection='3d')                                                   
f1_ax3 = fig1.add_subplot(1,3,3, projection='3d')
plot_sol(Upwind_s , f1_ax1, 'Upwind dx = {}; x* = {}; Gamma = {}'.format(Upwind_s.dx, Upwind_s.x_s, Upwind_s.gamma))               
plot_sol(filterUpwind_s, f1_ax2 ,  'Filtered Upwind dx={}; x* = {}; Gamma = {}'.format(filterUpwind_s.dx, filterUpwind_s.x_s, filterUpwind_s.gamma))
plot_sol(Exact_s, f1_ax3, 'Exact dx={}; x* = {}'.format(Exact_s.dx, Exact_s.x_s)) 

#figure 2
fig2 = plt.figure(plt.figure(figsize=plt.figaspect(0.5)))
f2_ax1 = fig2.add_subplot(1, 2, 1)
f2_ax1.plot(error_FUW_table["dx"].tolist(), error_FUW_table["t=1"].tolist())
f2_ax1.set_xlabel('dx', fontsize=12);   f2_ax1.set_ylabel('Error', fontsize=12);    f2_ax1.set_title('error plots at t = 1')

#top right f2
f2_ax2 = fig2.add_subplot(2, 2, 2)
xplots = {"Upwind" : f2_ax2.plot(np.linspace(0, 1, (Upwind_s.N)), get_xslice(Upwind_s.p, int(Upwind_s.M/2)))
          ,"Filtered Upwind" : f2_ax2.plot(np.linspace(0, 1, (filterUpwind_s.N)), get_xslice(filterUpwind_s.p, int(filterUpwind_s.M/2)))
            ,"Exact" : f2_ax2.plot(np.linspace(0, 1, (Exact_s.N)), get_xslice(Exact_s.p, int(Exact_s.M/2)))}
plt.legend(xplots);     f2_ax2.set_xlabel('t', fontsize=12);    f2_ax2.set_ylabel('denisity', fontsize=12);     f2_ax2.set_title('slice at t')

#bottom right f2
f2_ax3 = fig2.add_subplot(2, 2, 4)
tplots = {"Upwind" : f2_ax3.plot(np.linspace(0, 1, (Upwind_s.M)), get_tslice(Upwind_s.p, int(Upwind_s.N/2)))
          ,"Filtered Upwind" : f2_ax3.plot(np.linspace(0, 1, (filterUpwind_s.M)), get_tslice(filterUpwind_s.p, int(filterUpwind_s.N/2)))
            ,"Exact" : f2_ax3.plot(np.linspace(0, 1, (Exact_s.M)), get_tslice(Exact_s.p, int(Exact_s.N/2)))}
plt.legend(tplots);     f2_ax3.set_xlabel('x', fontsize=12);    f2_ax3.set_ylabel('denisity', fontsize=12);    f2_ax3.set_title('slice at x')

plt.subplots_adjust(wspace=.5, hspace=.8)
plt.show()
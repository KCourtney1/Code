import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from numba import njit

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
        self.dt = (1/(1+self.epsilon)) * (0.8 * ((2 - self.gamma) / (2 + self.gamma)) * self.dx)
        self.M = int(1/self.dx) + 1
        self.N = int(2/self.dt) + 1
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
        self.p[0, :] = self.IC                                                               #set matrix initial condition
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
        self.p[:, 0] = BC
        self.p[0, :] = IC

        for n in range(0, self.N - 1):
            for j in range(1, self.M):
                nu = self.get_vbar(j*dx) * (self.dt/self.dx)
                if n == 0:
                    self.p[n, j] = (1 - nu) * self.p[n, j] + nu * self.p[n, j-1]
                else:
                    self.p[n + 1, j] = (self.gamma + (1 - nu) * (1 - (self.gamma / 2))) * self.p[n, j] \
                                                            - (self.gamma / 2) * self.p[n - 1, j] \
                                                            + nu * (1 - (self.gamma / 2)) * self.p[n, j - 1]

def density_check(s, tolerance = 10**-5):
    time_level = 0
    happened = False
    for n in range(s.N):
        if np.isclose(s.p[n, -1], s.BC, tolerance) and not happened:
            t_time_level = n
            happened = True
    true_ATT =  s.x_s + (1/(1 +  s.epsilon) * (1 -  s.x_s))
    
    m_time_level = np.argmax(s.p[:, -1])
    
    m_est_ATT = m_time_level * s.dt
    t_est_ATT = t_time_level *  s.dt
    t_error = t_est_ATT - true_ATT
    m_error = m_est_ATT - true_ATT
    return [s.dt, epsilon, true_ATT, t_error, t_time_level, t_est_ATT, m_error, m_time_level, m_est_ATT]

dx = (2)**(-10)
BC = .47
IC = 0.0

with pd.ExcelWriter("ATT error tales.xlsx", engine="openpyxl") as writer:
    for gamma in [0, 1.75]:
        tables = []
        for x_s in [0.25, 0.5, 0.75]:
            error_table = []
            for epsilon in [0.1, 0.2, 0.3, 0.4, 0.5]:
                plots = [Upwind_s, filterUpwind_s, Exact_s] = [Upwind(dx, BC, IC, x_s, gamma, epsilon)
                                                                         , FilteredUpwind(dx, BC, IC, x_s, gamma, epsilon)
                                                                         , Exact(dx, BC, IC, x_s, gamma, epsilon)]
                Upwind_s.dt = (1/(1+epsilon)) * (0.8 * ((2 - 1.75) / (2 + 1.75)) * Upwind_s.dx)
                Exact_s.dt = (1/(1+epsilon)) * (0.8 * ((2 - 1.75) / (2 + 1.75)) * Exact_s.dx)
                filterUpwind_s.dt = (1/(1+epsilon)) * (0.8 * ((2 - 1.75) / (2 + 1.75)) * filterUpwind_s.dx)

                Upwind_s.update_p(); filterUpwind_s.update_p(); Exact_s.update_p()
                error_table.append(density_check(filterUpwind_s))
                density_error_table = pd.DataFrame(error_table, columns=["dt", "Epsilon","True ATT.", 
                                                                     "Tolerance ATT. Error", "Tolerance Time Level","Tolerance Est. ATT.",
                                                                       "Max ATT. Error", "Max Time Level", "Max Est. ATT."])
            metadata_values = pd.DataFrame([["gamma", "dx", "x_s"],[gamma, dx, x_s]])
            final_table = pd.concat([metadata_values, density_error_table], axis=0, ignore_index=True)
            tables.append(final_table)
        full_table = pd.concat(tables, ignore_index=True)
        full_table.to_excel(writer, sheet_name="gamma = {}".format(gamma), index=False)

def plot_sol(S, ax, title):
    X, T = np.meshgrid(np.linspace(0, 1, (S.M)), np.linspace(0, 1, (S.N)))
    ax.clear()
    ax.plot_surface(X, T, S.p, cmap='copper', edgecolor='none', alpha=0.8)    #colors = plasma, hot, jet, summer, copper
    ax.set_xlabel('x', fontsize=12);    ax.set_ylabel('t', fontsize=12);    ax.set_zlabel('z', fontsize=12);    ax.set_title(title)

#figure 1
def draw_next(event):
    global GraphIndex
    GraphIndex = (GraphIndex + 1) % len(plots)
    ax1.clear()
    plot_sol(plots[GraphIndex], ax1, '{} at dx = {}; dt = {}; x* = {}; Gamma = {}'.format(str(plots[GraphIndex]), plots[GraphIndex].dx, plots[GraphIndex].dt, plots[GraphIndex].x_s, plots[GraphIndex].gamma))
    plt.draw()

def draw_prev(event):
    global GraphIndex
    GraphIndex = (GraphIndex - 1) % len(plots)
    ax1.clear()
    plot_sol(plots[GraphIndex], ax1, '{} at dx = {}; dt = {}; x* = {}; Gamma = {}'.format(str(plots[GraphIndex]), plots[GraphIndex].dx, plots[GraphIndex].dt, plots[GraphIndex].x_s, plots[GraphIndex].gamma))
    plt.draw()

GraphIndex = 0
fig1 = plt.figure(figsize=plt.figaspect(.7))
ax1 = fig1.add_subplot(111, projection='3d')
plot_sol(plots[0], ax1, '{} at dx = {}; dt = {}; x* = {}; Gamma = {}'.format(str(plots[0]), plots[0].dx, plots[GraphIndex].dt, plots[0].x_s, plots[0].gamma))
button_next = Button(plt.axes([0.85, 0.01, 0.1, 0.05]), 'Next');        button_next.on_clicked(draw_next)
button_prev = Button(plt.axes([0.05, 0.01, 0.1, 0.05]), 'Previous');    button_prev.on_clicked(draw_prev)

plt.show()
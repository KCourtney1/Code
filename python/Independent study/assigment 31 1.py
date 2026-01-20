import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.widgets import Slider
from matplotlib.widgets import CheckButtons
from scipy.sparse.linalg import spsolve
from scipy.sparse import diags, csr_matrix
import time

class Exact:
    def __init__(self, dx, BC, IC, gamma, epsilon) -> None:
        self.gamma = gamma
        self.dx = dx
        self.BC = BC
        self.IC = IC
        self.epsilon = epsilon

    def __str__(self):
        return "Exact"

    @property
    def dx(self):
        return self._dx

    @dx.setter
    def dx(self, dx):
        self._dx = dx
        self.dt = dx #(1/(1+self.epsilon)) * (0.8 * ((2 - self.gamma) / (2 + self.gamma)) * self.dx)
        self.M = int(1/self.dx) + 1
        self.N = int(1/self.dt) + 1
        self.p = np.zeros((self.N, self.M))
        self.x_s = self.M // 2 + 1

    def update_p(self):
        for n in range(self.N):  # time loop
            for j in range(self.M):  # space loop
                t = n * self.dt
                x = j * self.dx
                self.x_s = .5
                if ((0 <= x <= self.x_s) and (t <= x)) or ((self.x_s <= x <= 1) and (t < ((1/(1 + self.epsilon)) * (x - self.x_s) + self.x_s))):
                    self.p[n, j] = self.IC
                else:
                    self.p[n, j] = self.BC
 

class implicit(Exact):
    def __init__(self, dx, BC, IC, gamma, epsilon) -> None:
        super().__init__(dx, BC, IC, gamma, epsilon)

    def __str__(self):
        return "Implicit"
    
    def get_coefficient_m_standard(self):
        nu = np.ones(self.M)
        nu[self.x_s:] += (1/(1+self.epsilon))
        nu = nu * (self.dt/self.dx)

        main_diag_value = 1 + nu
        sub_diag_value = -nu[1:]

        main_diag = np.full(self.M, main_diag_value)
        sub_diag = np.full(self.M - 1, sub_diag_value)
        return diags([main_diag, sub_diag], [0, -1], format='csr')

    def get_p_hat(self, n):
        array = self.p[n, :]
        return array

    def update_p(self):
        self.p[:, 0] = self.BC
        self.p[0, 1:] = self.IC   
        
        for n in range(0, self.N - 1):
            rhs = self.get_p_hat(n + 1) + self.p[n, :]         
            self.p[n + 1, :] = spsolve(self.get_coefficient_m_standard(), rhs)

class filteredImplicit(implicit):
    def __init__(self, dx, BC, IC, gamma, epsilon) -> None:
        super().__init__(dx, BC, IC, gamma,  epsilon)
    
    def __str__(self):
        return "Filtered_Implicit"
    
    def get_coefficient_m_filtered(self):
        nu = np.ones(self.M)
        nu[self.x_s:] += (1/(1+self.epsilon))
        nu = nu * (self.dt/self.dx)

        main_diag = (2 / (2 - self.gamma)) + nu
        sub_diag = -nu[1:]
        A = diags([main_diag, sub_diag], [0, -1], format='csr')
        return A

    def update_p(self):
        self.p[:, 0] = self.BC                                                               #set matrix boundary condition
        self.p[0, 1:] = self.IC   
        nu = self.dt/self.dx

        rhs = self.get_p_hat(1) + self.p[0, :]
        self.p[1, :] = spsolve(implicit.get_coefficient_m_standard(self), rhs)
        if gamma == 0:
            implicit.update_p(self)
        else:
            for n in range(1, self.N - 1):
                rhs = (nu * self.get_p_hat(n + 1)) + ((1 + ((2 * self.gamma) / (2 - self.gamma))) * self.p[n, :]) - ((self.gamma / (2 - self.gamma)) * self.p[n - 1, :])
                self.p[n + 1, :] = spsolve(self.get_coefficient_m_filtered(), rhs)

def rate_of_convergence(error_table):
    rates = []
    for i in range(1, len(error_table)):
        dx1 = error_table.iloc[i-1, 0]       #second is position in the table
        dx2 = error_table.iloc[i, 0]
        error1 = error_table.iloc[i-1, -1]   #i, use t = 1 and then change gamma
        error2 = error_table.iloc[i, -1]     #i + 1
        rate = np.log(error1 / error2) / np.log(dx1 / dx2)
        rates.append(rate)
    return rates

def density_check(s, tolerance = 10**-3):
    matches = np.isclose(s.p[:, -s.M//2], s.BC, atol=tolerance)
    if np.any(matches):
        t_time_level = np.argmax(matches)
    else:
        t_time_level =  -1

    if gamma != 0:
        true_ATT = 0.5 + (1/(1 +  s.epsilon) * (1 -  0.5))
    else:
        true_ATT = 1
    
    m_time_level = np.argmax(s.p[:, -1])

    m_est_ATT = m_time_level * s.dt
    t_est_ATT = t_time_level *  s.dt
    t_error = t_est_ATT - true_ATT
    m_error = m_est_ATT - true_ATT
    return [s.dt, true_ATT, t_error, t_time_level, t_est_ATT, m_error, m_time_level, m_est_ATT]

def error(approx, exact, tvalues = [0, .2, .4, .6, .8, 1]):
    tval_errors = []
    for t_val in tvalues:
        n = int(t_val/exact.dt) + 1
        if n >= exact.N:
            n = exact.N - 1
        error = np.abs(approx.p[n, :] - exact.p[n, :])
        tval_errors.append(np.sum(error)*exact.dt)
    return tval_errors

start_time = time.time()

BC = .47
IC = 0.0
gamma_values = [0, 0.25, 0.5, 0.75, .9]
epsilon_values = [0.1, 0.2, 0.3, 0.4, 0.5]

filtered_implicit_error_dataframes = []
error_table = []

for gamma in gamma_values:
    for epsilon in epsilon_values:
        dx_implicit_error = []
        dx_filtered_upwind_error = []
        error_table = []
        for i in range(6, 8):
            dx = (1/2)**(i)
            plots = [implicit_s, filtered_implicit_s, Exact_s] = [implicit(dx, BC, IC, gamma, epsilon),
                                                                                filteredImplicit(dx, BC, IC, gamma, epsilon), 
                                                                                Exact(dx, BC, IC, gamma, epsilon)]
            implicit_s.update_p()
            filtered_implicit_s.update_p()
            Exact_s.update_p()

            dx_filtered_upwind_error.append([dx] + [gamma] + [epsilon] + error(filtered_implicit_s, Exact_s))
            dx_implicit_error.append([dx] + [gamma] + [epsilon] + error(implicit_s, Exact_s))
            error_table.append(density_check(filtered_implicit_s))

        error_implicit_table = pd.DataFrame(dx_implicit_error, columns=["dx", "gamma", "epsilon","t=0", "t=0.2", "t=0.4", "t=0.6", "t=0.8", "t=1"])
        density_error_table = pd.DataFrame(error_table, columns=["dt","True ATT.", "Tolerance ATT. Error", "Tolerance Time Level","Tolerance Est. ATT.",
                                                                "Max ATT. Error", "Max Time Level", "Max Est. ATT."])
        with pd.ExcelWriter("implicit error table gamma = {}.xlsx".format(gamma), engine="openpyxl") as writer:
            error_implicit_table.to_excel(writer, sheet_name="Epsilon = {}".format(epsilon))
            density_error_table.to_excel(writer, sheet_name="Density Error Table = {}".format(epsilon))
        
        error_filtered_implicit_table = pd.DataFrame(dx_filtered_upwind_error, columns=["dx", "gamma", "epsilon", "t=0", "t=0.2", "t=0.4", "t=0.6", "t=0.8", "t=1"])
        density_error_table = pd.DataFrame(error_table, columns=["dt","True ATT.", "Tolerance ATT. Error", "Tolerance Time Level","Tolerance Est. ATT.",
                                                                "Max ATT. Error", "Max Time Level", "Max Est. ATT."])
        with pd.ExcelWriter("filtered implicit error table gamma = {}.xlsx".format(gamma), engine="openpyxl") as writer:
            error_filtered_implicit_table.to_excel(writer, sheet_name="Epsilon ={}".format(epsilon))
            filtered_implicit_error_dataframes.append(error_filtered_implicit_table)
            density_error_table.to_excel(writer, sheet_name="Density Error Table ε = {}".format(epsilon))

        roc = rate_of_convergence(error_filtered_implicit_table)
        roc_df = pd.DataFrame(roc, columns=["ROC"])
        with pd.ExcelWriter("Filtered ROC Table gamma = {}.xlsx".format(gamma), engine="openpyxl") as writer:
            roc_df.to_excel(writer, sheet_name="ROC for epsilon = {}".format(epsilon))

end_time = time.time()
print("Execution time: {:.2f} seconds".format(end_time - start_time))

def plot_sol(S, ax, title):
    X, T = np.meshgrid(np.linspace(0, 1, (S.M)), np.linspace(0, 1, (S.N)))
    ax.clear()
    ax.plot_surface(X, T, S.p, cmap='copper', edgecolor='none', alpha=0.8)    #colors = plasma, hot, jet, summer, copper
    ax.set_xlabel('x', fontsize=12);    ax.set_ylabel('t', fontsize=12);    ax.set_zlabel('z', fontsize=12);    ax.set_title(title)

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
f2_ax1.set_xlabel('ln(dx)', fontsize=12); f2_ax1.set_ylabel('ln(error)', fontsize=12); f2_ax1.set_title('log-log Error at t=0.4')
f2_ax2.set_xlabel('ln(dx)', fontsize=12); f2_ax2.set_ylabel('ln(error)', fontsize=12); f2_ax2.set_title('log-log Error at t=1')

for i in range(len(filtered_implicit_error_dataframes)):
    df = filtered_implicit_error_dataframes[i]
    df_gamma = df["gamma"].values[0]
    dx = np.log(df["dx"].values)
    t_4 = np.log(df["t=0.4"].values)
    t_1 = np.log(df["t=1"].values)
    f2_ax1.plot(dx, t_4, 'o-', label="gamma = {}".format(df_gamma))
    f2_ax2.plot(dx, t_1, 'o-', label="gamma = {}".format(df_gamma))
f2_ax1.legend(); f2_ax2.legend()

#figure 3
fig3 = plt.figure(figsize=plt.figaspect(0.5))
f3_ax1 = fig3.add_subplot(121)
f3_ax2 = fig3.add_subplot(122)
f3_ax1.set_xlabel('dx', fontsize=12); f3_ax1.set_ylabel('error', fontsize=12); f3_ax1.set_title('Filtered Implicit Error at t=0.4')
f3_ax2.set_xlabel('dx', fontsize=12); f3_ax2.set_ylabel('error', fontsize=12); f3_ax2.set_title('Filtered Implicit Error at t=1')

for i in range(len(filtered_implicit_error_dataframes)):
    df = filtered_implicit_error_dataframes[i]
    df_gamma = df["gamma"].values[0]
    dx = df["dx"].values
    t_4 = df["t=0.4"].values
    t_1 = df["t=1"].values
    f3_ax1.plot(dx, t_4, 'o-', label="gamma = {}".format(df_gamma))
    f3_ax2.plot(dx, t_1, 'o-', label="gamma = {}".format(df_gamma))
f3_ax1.legend(); f3_ax2.legend()

plt.show()
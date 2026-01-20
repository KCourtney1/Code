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
        self.dt = dx #(1/(1+self.epsilon)) * (0.8 * ((2 - self.gamma) / (2 + self.gamma)) * self.dx)
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
                if t < x <= 1: #((0 <= x <= self.x_s) and (x > t)) or ((self.x_s <= x <= 1) and (t<=(1/(1+self.epsilon)*(x-self.x_s)+self.x_s)))
                    self.p[n,j] = self.IC
                else:
                    self.p[n,j] = self.BC 

class Upwind(Exact):
    def __init__(self, dx, BC, IC, x_s, gamma, epsilon) -> None:
        super().__init__(dx, BC, IC, x_s, gamma, epsilon)

    def __str__(self):
        return "Upwind"

    def update_p(self):
        self.p[:, 0] = self.BC 
        self.p[0, 1:] = self.IC
        for n in range(self.N - 1):
            for j in range(1, self.M):
                nu = self.get_vbar(j*self.dx) * (self.dt / self.dx)
                self.p[n+1, j] = (1 - nu) * self.p[n, j] + nu * self.p[n, j-1]

class implicit(Exact):
    def __init__(self, dx, BC, IC, x_s, gamma, epsilon) -> None:
        super().__init__(dx, BC, IC, x_s, gamma, epsilon)

    def __str__(self):
        return "Implicit"
    
    def get_coefficient_m_standard(self):
        nu = self.dt/self.dx

        main_diag = np.full(self.M, 1 + nu)
        sub_diag = np.full(self.M - 1, -nu)
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
    def __init__(self, dx, BC, IC, x_s, gamma, epsilon) -> None:
        super().__init__(dx, BC, IC, x_s, gamma, epsilon)
    
    def __str__(self):
        return "Filtered_Implicit"
    
    def get_coefficient_m_filtered(self):
        nu = self.dt / self.dx

        main_diag_value = (2 / (2 - self.gamma)) + nu
        main_diag = np.full(self.M, main_diag_value)
        sub_diag_value = -nu
        sub_diag = np.full(self.M - 1, sub_diag_value)
        return diags([main_diag, sub_diag], [0, -1], format='csr')
    
    def update_p(self):
        self.p[:, 0] = self.BC                                                               #set matrix boundary condition
        self.p[0, 1:] = self.IC   
        nu = self.dt/self.dx

        rhs = self.get_p_hat(1) + self.p[0, :]
        self.p[1, :] = spsolve(implicit.get_coefficient_m_standard(self), rhs)
        for n in range(1, self.N - 1):
            rhs = (nu * self.get_p_hat(n + 1)) + ((1 + ((2 * self.gamma) / (2 - self.gamma))) * self.p[n, :]) - ((self.gamma / (2 - self.gamma)) * self.p[n - 1, :])
            self.p[n + 1, :] = spsolve(self.get_coefficient_m_filtered(), rhs)

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
x_s = 0
epsilon = 0
gamma_values = [0, 0.5, 0.75, 1.0]  #gamma values to test

slices_t = []
slices_x = []
filtered_implicit_error_dataframes = []
for gamma in gamma_values:
    dx_implicit_error = []
    dx_filtered_upwind_error = []
    for i in range(4, 10):
        dx = (1/2)**(i)
        plots = [Upwind_s, implicit_s, filtered_implicit_s, Exact_s] = [Upwind(dx, BC, IC, x_s, gamma, epsilon), 
                                                                            implicit(dx, BC, IC, x_s, gamma, epsilon),
                                                                            filteredImplicit(dx, BC, IC, x_s, gamma, epsilon), 
                                                                            Exact(dx, BC, IC, x_s, gamma, epsilon)]
        Upwind_s.update_p()
        implicit_s.update_p()
        filtered_implicit_s.update_p()
        Exact_s.update_p()

        dx_filtered_upwind_error.append([dx] + [gamma] + error(filtered_implicit_s, Exact_s))
        dx_implicit_error.append([dx] + [gamma] + error(implicit_s, Exact_s))
    slices_t.append(filtered_implicit_s.p[:, Exact_s.M//2])
    slices_x.append(filtered_implicit_s.p[Exact_s.N//2, :])

    with pd.ExcelWriter("implicit error table gamma = {}.xlsx".format(gamma), engine="openpyxl") as writer:
        error_implicit_table = pd.DataFrame(dx_implicit_error, columns=["dx", "gamma", "t=0", "t=0.2", "t=0.4", "t=0.6", "t=0.8", "t=1"])
        error_implicit_table.to_excel(writer, sheet_name="Implicit Error Table")

        error_filtered_implicit_table = pd.DataFrame(dx_filtered_upwind_error, columns=["dx", "gamma", "t=0", "t=0.2", "t=0.4", "t=0.6", "t=0.8", "t=1"])
        error_filtered_implicit_table.to_excel(writer, sheet_name="Filtered Implicit Error Table")
        filtered_implicit_error_dataframes.append(error_filtered_implicit_table)

end_time = time.time()
print("Execution time: {:.2f} seconds".format(end_time - start_time))

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
    plot_sol(plots[GraphIndex], ax1, '{} at dx = {}; dt = {};'.format(str(plots[GraphIndex]), plots[GraphIndex].dx, plots[GraphIndex].dt))
    plt.draw()

def draw_prev(event):
    global GraphIndex
    GraphIndex = (GraphIndex - 1) % len(plots)
    ax1.clear()
    plot_sol(plots[GraphIndex], ax1, '{} at dx = {}; dt = {};'.format(str(plots[GraphIndex]), plots[GraphIndex].dx, plots[GraphIndex].dt))
    plt.draw()

def update_slider_Xgraph(event):
    f2_ax1.clear()
    D_t = np.linspace(0, 1, (Exact_s.N))
    if line_visibility["Upwind"]:
        f2_ax1.plot(D_t, Upwind_s.p[:,f2_ax1_Slider.val], label="Upwind")
    if line_visibility["Implicit"]:
        f2_ax1.plot(D_t, implicit_s.p[:,f2_ax1_Slider.val], label="Implicit")
    if line_visibility["Filtered Implicit"]:
        f2_ax1.plot(D_t, filtered_implicit_s.p[:, f2_ax1_Slider.val], label="Filtered Implicit")   
    if line_visibility["Exact"]:
        f2_ax1.plot(D_t, Exact_s.p[:,f2_ax1_Slider.val], label="Exact")
    f2_ax1.legend()
    f2_ax1.set_xlabel('x', fontsize=12); f2_ax1.set_ylabel('density', fontsize=12); f2_ax1.set_title('slice at t')
    plt.draw()

def update_slider_Tgraph(event):
    f2_ax2.clear()
    D_x = np.linspace(0, 1, (Exact_s.M))
    if line_visibility["Upwind"]:
        f2_ax2.plot(D_x, Upwind_s.p[f2_ax2_Slider.val, :], label="Upwind")
    if line_visibility["Implicit"]:
        f2_ax2.plot(D_x, implicit_s.p[f2_ax2_Slider.val, :], label="Implicit")
    if line_visibility["Filtered Implicit"]:
        f2_ax2.plot(D_x, filtered_implicit_s.p[f2_ax2_Slider.val, :], label="Filtered Implicit")    
    if line_visibility["Exact"]:
        f2_ax2.plot(D_x, Exact_s.p[f2_ax2_Slider.val, :], label="Exact")
    f2_ax2.legend()
    f2_ax2.set_xlabel('t', fontsize=12); f2_ax2.set_ylabel('density', fontsize=12); f2_ax2.set_title('slice at x')
    plt.draw()

def update_lines(label):
    line_visibility[label] = not line_visibility[label]
    update_slider_Xgraph(None)
    update_slider_Tgraph(None)


#figure 1
GraphIndex = 0
fig1 = plt.figure(figsize=plt.figaspect(.7))
ax1 = fig1.add_subplot(111, projection='3d')
plot_sol(plots[0], ax1, '{} at dx = {}; dt = {}'.format(str(plots[0]), plots[0].dx, plots[GraphIndex].dt))
button_next = Button(plt.axes([0.85, 0.01, 0.1, 0.05]), 'Next');        button_next.on_clicked(draw_next)
button_prev = Button(plt.axes([0.05, 0.01, 0.1, 0.05]), 'Previous');    button_prev.on_clicked(draw_prev)

#figure 2
line_visibility = {"Upwind": True, "Implicit": True, "Filtered Implicit": True, "Exact": True}
fig2 = plt.figure(figsize=plt.figaspect(0.5))
f2_ax1 = fig2.add_subplot(2, 1, 1)#top right f2
f2_ax1_Slider = Slider(plt.axes([0.915, .25, .025, .6]), label="M", valmin=0, valmax=Exact_s.M-1, valstep=1, orientation="vertical"); f2_ax1_Slider.on_changed(update_slider_Xgraph)
f2_ax2 = fig2.add_subplot(2, 1, 2)#bottom right f2
f2_ax2_Slider = Slider(plt.axes([0.965, .25, .025, .6]), label="N", valmin=0, valmax=Exact_s.N-1, valstep=1, orientation="vertical"); f2_ax2_Slider.on_changed(update_slider_Tgraph)

rax = plt.axes([0.90, 0.11, 0.1, 0.10])
check = CheckButtons(rax, ("Upwind", "Implicit", "Filtered Implicit", "Exact"), (True, True, True, True))
check.on_clicked(update_lines)

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

#figure 4
fig4 = plt.figure(figsize=plt.figaspect(0.5))
f4_ax1 = fig4.add_subplot(121); f4_ax1.set_xlabel("t"); f4_ax1.set_ylabel('density'); f4_ax1.set_title('slice at x = 0.5')
f4_ax2 = fig4.add_subplot(122); f4_ax2.set_xlabel("x"); f4_ax2.set_ylabel('density'); f4_ax2.set_title('slice at t = 0.5')
for i in range(len(slices_t)):
    f4_ax1.plot(np.linspace(0, 1, Exact_s.M), slices_x[i], label="gamma = {}".format(gamma_values[i]))
    f4_ax2.plot(np.linspace(0, 1, Exact_s.N), slices_t[i], label="gamma = {}".format(gamma_values[i]))
f4_ax1.legend(); f4_ax2.legend()

plt.show()
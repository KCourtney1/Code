import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.widgets import Slider
from matplotlib.widgets import CheckButtons

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
        self.p[:, 0] = self.BC                                                               #set matrix boundary condition
        self.p[0, 1:] = self.IC                                                               #set matrix initial condition
        for n in range(self.N - 1):
            for j in range(1, self.M):
                nu = self.get_vbar(j*self.dx) * (self.dt / self.dx)
                self.p[n+1, j] = (1 - nu) * self.p[n, j] + nu * self.p[n, j-1]              #set density at point P[n+1][j];  p[n+1, j] = (1 - nu) * p[n, j] + nu * p[n, j-1]

class implicit(Exact):
    def __init__(self, dx, BC, IC, x_s, gamma, epsilon) -> None:
        super().__init__(dx, BC, IC, x_s, gamma, epsilon)
        self.coefficient_m = self.get_coefficient_m()

    def __str__(self):
        return "implicit"
    
    def get_coefficient_m(self):
        N = self.N
        main_diag = np.diag(np.full(N, 2.0)) 
        sub_diag = np.diag(np.full(N - 1, -1.0), k=-1)
        m = main_diag + sub_diag
        return m

    def get_p_hat(self, n):
        array = np.zeros(self.N)
        array[0] = self.p[n+1, 0]
        return array

    def update_p(self):
        self.p[:, 0] = self.BC                                                               #set matrix boundary condition
        self.p[0, 1:] = self.IC   

        inv = np.linalg.inv(self.coefficient_m)
        for n in range(0, self.N - 1):
            self.p[n+1, :] = inv @ (implicit.get_p_hat(self, n) + self.p[n, :])

def error(approx, exact, tvalues = [0, .2, .4, .6, .8, 1]):
    tval_errors = []
    for t_val in tvalues:
        n = int(t_val/exact.dx)
        error = np.abs(approx.p[n, :] - exact.p[n, :])
        tval_errors.append(np.sum(error)*exact.dx)
    return tval_errors

BC = .47
IC = 0.0
x_s = 0.5
epsilon = 0
gamma = 0

dx_implicit_error = []
dx_upwind_error = []
for i in range(10, 11):
    dx = (1/2)**(i)
    plots = [Upwind_s, implicit_s, Exact_s] = [Upwind(dx, BC, IC, x_s, gamma, epsilon), 
                                               implicit(dx, BC, IC, x_s, gamma, epsilon), 
                                               Exact(dx, BC, IC, x_s, gamma, epsilon)]
    Upwind_s.update_p()
    implicit_s.update_p()
    Exact_s.update_p()
    
    dx_implicit_error.append([dx] + error(implicit_s, Exact_s))
    dx_upwind_error.append([dx] + error(Upwind_s, Exact_s))

with pd.ExcelWriter("implicit solution error table.xlsx", engine="openpyxl") as writer:
    error_implicit_table = pd.DataFrame(dx_implicit_error, columns=["dx","t=0", "t=0.2", "t=0.4", "t=0.6", "t=0.8", "t=1"])
    error_implicit_table.to_excel(writer, sheet_name="Implicit Error Table")
    error_upwind_table = pd.DataFrame(dx_upwind_error, columns=["dx","t=0", "t=0.2", "t=0.4", "t=0.6", "t=0.8", "t=1"])
    error_upwind_table.to_excel(writer, sheet_name="Upwind Error Table")


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

GraphIndex = 0
fig1 = plt.figure(figsize=plt.figaspect(.7))
ax1 = fig1.add_subplot(111, projection='3d')
plot_sol(plots[0], ax1, '{} at dx = {}; dt = {}'.format(str(plots[0]), plots[0].dx, plots[GraphIndex].dt))
button_next = Button(plt.axes([0.85, 0.01, 0.1, 0.05]), 'Next');        button_next.on_clicked(draw_next)
button_prev = Button(plt.axes([0.05, 0.01, 0.1, 0.05]), 'Previous');    button_prev.on_clicked(draw_prev)


def update_slider_Xgraph(event):
    f2_ax1.clear()
    D_t = np.linspace(0, 1, (Exact_s.N))
    if line_visibility["Upwind"]:
        f2_ax1.plot(D_t, Upwind_s.p[:,f2_ax1_Slider.val], label="Upwind")
    if line_visibility["Implicit"]:
        f2_ax1.plot(D_t, implicit_s.p[:,f2_ax1_Slider.val], label="Implicit")
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
    if line_visibility["Exact"]:
        f2_ax2.plot(D_x, Exact_s.p[f2_ax2_Slider.val, :], label="Exact")
    f2_ax2.legend()
    f2_ax2.set_xlabel('t', fontsize=12); f2_ax2.set_ylabel('density', fontsize=12); f2_ax2.set_title('slice at x')
    plt.draw()

fig2 = plt.figure(plt.figure(figsize=plt.figaspect(0.5)))
f2_ax1 = fig2.add_subplot(2, 1, 1)#top right f2
f2_ax1_Slider = Slider(plt.axes([0.915, .25, .025, .6]), label="M", valmin=0, valmax=Exact_s.M-1, valstep=1, orientation="vertical"); f2_ax1_Slider.on_changed(update_slider_Xgraph)
f2_ax2 = fig2.add_subplot(2, 1, 2)#bottom right f2
f2_ax2_Slider = Slider(plt.axes([0.965, .25, .025, .6]), label="N", valmin=0, valmax=Exact_s.N-1, valstep=1, orientation="vertical"); f2_ax2_Slider.on_changed(update_slider_Tgraph)

line_visibility = {"Upwind": True, "Implicit": True, "Exact": True}
rax = plt.axes([0.90, 0.11, 0.1, 0.10])
check = CheckButtons(rax, ("Upwind", "Implicit", "Exact"), (True, True, True))
def update_lines(label):
    line_visibility[label] = not line_visibility[label]
    update_slider_Xgraph(None)
    update_slider_Tgraph(None)
check.on_clicked(update_lines)

plt.show()
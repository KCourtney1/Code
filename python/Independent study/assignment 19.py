import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.widgets import Slider

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

class Tracer(Exact):
    def __init__(self, dx, BC, IC, x_s, gamma, epsilon) -> None:
        super().__init__(dx, BC, IC, x_s, gamma, epsilon)

    def __str__(self):
        return "Tracer"

    def Trace_point(self, x_bar, t_bar): # returns t* based on region and point
        if (x_bar < self.x_s) and (t_bar >= x_bar):
            return t_bar - x_bar
        elif (x_bar >= x_s) and (t_bar > (x_s + (1 / (1 + self.epsilon) * (x_bar - x_s)))):
            return (t_bar - 1 / (1 + self.epsilon) * (x_bar + self.epsilon * x_s))
        return 0

    def Final_time(self, x_s):
        return x_s + (1/(1+self.epsilon) * (1 - x_s))

    def final_n_times(start, stop):
        Final_times=[]
        for p in range(start, stop):
            n = 10**p
            Final_times.append([n, tracer_s.Final_time(.25), tracer_s.Final_time(.5), tracer_s.Final_time(.75)])
        return Final_times

    def update_p(self):     # at given point z(x,t) = t*
        for n in range(self.N):
            for j in range(self.M):
                t = n * self.dt
                x = j * self.dx
                self.p[n,j] = self.Trace_point(x, t)

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

def density_check(FUW_s):
    ATT_est = 0
    happened = False
    for n in range(FUW_s.N):
        if np.isclose(FUW_s.p[n, -1], FUW_s.BC, 0.001) and not happened:
            ATT_est = n
            happened = True
    print(FUW_s.p[ATT_est, -1])     
    print(ATT_est)
    return ATT_est *  FUW_s.dt - ( FUW_s.x_s + (1/(1 +  FUW_s.epsilon) * (1 -  FUW_s.x_s)))

def error(approx, exact, tvalues = [0, .2, .4, .6, .8, 1]):
    tval_errors = []
    for t_val in tvalues:
        n = int(t_val/approx.dt)
        if n >= len(approx.p):
            n = len(approx.p) - 1

        error = np.abs(approx.p[n, :] - exact.p[n, :])
        tval_errors.append(np.sum(error)*approx.dx)
    return tval_errors

dx_UW_error, dx_FUW_error = [],[]
for i in range(8, 9):
    dx = (2)**(-i)
    BC = .47
    IC = 0.0

    epsilon = .1            # 0.0 <= epsilon <= 0.5
    gamma = 0
    x_s = 1/2

    plots = [Upwind_s, filterUpwind_s, Exact_s] = [Upwind(dx, BC, IC, x_s, gamma, epsilon)
                                                             , FilteredUpwind(dx, BC, IC, x_s, gamma, epsilon)
                                                             , Exact(dx, BC, IC, x_s, gamma, epsilon)]
    tracer_s = Tracer(dx, BC, IC, x_s, gamma, epsilon)
    Upwind_s.update_p(); filterUpwind_s.update_p(); Exact_s.update_p(); tracer_s.update_p()
    dx_UW_error.append([dx] + error(Upwind_s, Exact_s))
    dx_FUW_error.append([dx] + error(filterUpwind_s, Exact_s))

error_UW_table = pd.DataFrame(dx_UW_error, columns=["dx","t=0", "t=0.2", "t=0.4", "t=0.6", "t=0.8", "t=1"])
error_FUW_table = pd.DataFrame(dx_FUW_error, columns=["dx","t=0", "t=0.2", "t=0.4", "t=0.6", "t=0.8", "t=1"])
tracer_table = pd.DataFrame(tracer_s.p)
Final_time_table = pd.DataFrame(Tracer.final_n_times(2,5), columns=["n","x*=.25", "x*=.5", "x*=.75"]); 
with pd.ExcelWriter("tables_ε={}.xlsx".format(tracer_s.epsilon), engine="openpyxl") as writer:
    error_UW_table.to_excel(writer, sheet_name="Upwind Error")
    error_FUW_table.to_excel(writer, sheet_name="Filtered Upwind Error")
    tracer_table.to_excel(writer, sheet_name="tracer_table_ε={}".format(tracer_s.epsilon))
    Final_time_table.to_excel(writer, sheet_name="T_final_ε={}".format(tracer_s.epsilon))

print(str(density_check(filterUpwind_s))+"\n")
print(density_check(Upwind_s))

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

#figure 2
def update_slider_Xgraph(event):
    f2_ax2.clear()
    D_t = np.linspace(0, 1, (Exact_s.N))
    f2_ax2.plot(D_t, Upwind_s.p[:,f2_ax2_Slider.val])
    f2_ax2.plot(D_t, filterUpwind_s.p[:,f2_ax2_Slider.val])
    f2_ax2.plot(D_t, Exact_s.p[:,f2_ax2_Slider.val])
    f2_ax2.legend(["Upwind", "Filtered Upwind", "Exact"])
    f2_ax2.set_xlabel('x', fontsize=12);    f2_ax2.set_ylabel('denisity', fontsize=12);     f2_ax2.set_title('slice at t')
    plt.draw()

def update_slider_Tgraph(event):
    f2_ax4.clear()
    D_x = np.linspace(0, 1, (Exact_s.M))
    f2_ax4.plot(D_x, Upwind_s.p[f2_ax4_Slider.val, :])
    f2_ax4.plot(D_x, filterUpwind_s.p[f2_ax4_Slider.val, :])
    f2_ax4.plot(D_x, Exact_s.p[f2_ax4_Slider.val, :])
    f2_ax4.legend(["Upwind", "Filtered Upwind", "Exact"])
    f2_ax4.set_xlabel('t', fontsize=12);    f2_ax4.set_ylabel('denisity', fontsize=12);    f2_ax4.set_title('slice at x')
    plt.draw()

def update_slider_ErrGraph(event):
    f2_ax1.clear()
    f2_ax3.clear()
    f2_ax1.plot(error_FUW_table["dx"].tolist(), error_FUW_table["t={}".format(round(f2_ax13_Slider.val, 2))].tolist())
    f2_ax3.plot(error_UW_table["dx"].tolist(), error_UW_table["t={}".format(round(f2_ax13_Slider.val, 2))].tolist())
    f2_ax1.set_xlabel('dx', fontsize=12);   f2_ax1.set_ylabel('Error', fontsize=12);    f2_ax1.set_title('Filtered error plots at t = {}'.format(round(f2_ax13_Slider.val, 2)))
    f2_ax3.set_xlabel('dx', fontsize=12);   f2_ax3.set_ylabel('Error', fontsize=12);    f2_ax3.set_title('Upwind error plots at t = {}'.format(round(f2_ax13_Slider.val, 2)))
    plt.draw()

fig2 = plt.figure(plt.figure(figsize=plt.figaspect(0.5)))
f2_ax1 = fig2.add_subplot(2, 2, 1)
f2_ax3 = fig2.add_subplot(2, 2, 3)
f2_ax13_Slider = Slider(plt.axes([0.49, .1, .025, .8]), label="t", valmin=0, valmax=1, valstep=.2, orientation="vertical"); f2_ax13_Slider.on_changed(update_slider_ErrGraph)

f2_ax2 = fig2.add_subplot(2, 2, 2)#top right f2
f2_ax2_Slider = Slider(plt.axes([0.925, .1, .025, .8]), label="M", valmin=0, valmax=Exact_s.M-1, valstep=1, orientation="vertical"); f2_ax2_Slider.on_changed(update_slider_Xgraph)

f2_ax4 = fig2.add_subplot(2, 2, 4)#bottom right f2
f2_ax4_Slider = Slider(plt.axes([0.950, .1, .025, .8]), label="N", valmin=0, valmax=Exact_s.N-1, valstep=1, orientation="vertical"); f2_ax4_Slider.on_changed(update_slider_Tgraph)

# figure 3
fig3 = plt.figure(figsize=plt.figaspect(.5))
for i in range(0, len(plots)):
    plot_sol(plots[i], fig3.add_subplot(1, 3, i+1, projection='3d'), '{}'.format(str(plots[i])))

plt.show()
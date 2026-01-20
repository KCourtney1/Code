import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BC = .47
IC = 0.0
gamma = 1.75      # 0.0 <= gamma <= 2.0

def upwind():
    p = np.zeros((N, M))    #initilize matrix (M, N) of zeros
    p[:, 0] = BC            #set matrix boundary condition
    p[0, :] = IC            #set matrix initial condition

    for n in range(N - 1):
        for j in range(1, M):
            p[n+1, j] = (1 - nu) * p[n, j] + nu * p[n, j-1]     #set density at point P[n+1][j]
    return p

def filtered_upwind():
    p = np.zeros((N, M))    #initilize matrix (M, N) of zeros
    p[:, 0] = BC            #set matrix boundary condition
    p[0, :] = IC            #set matrix initial condition

    for n in range(N - 1):
        for j in range(1, M):
            p[n + 1, j] = (gamma + (1 - nu) * (1 - gamma/2)) * p[n, j] - gamma/2 * p[n - 1, j] + nu * (1 - gamma/2) * p[n , j - 1]          #upwind with additional maths to make it cooler
    return p

def Exact():
    # have v bar defined inside for loops? could? or just figure out the actual for piecewise
    p = np.zeros((N, M))
    for n in range(N):
        for j in range(M):
            t = n * dt
            x = j * dx
            if x < t:
                p[n, j] = 0.47
            else:
                p[n, j] = 0
    return p

def plot_sol(P, ax, title):
    x = np.linspace(0, 1, (M))
    t = np.linspace(0, 1, (N))
    X, T = np.meshgrid(x, t)

    ax.plot_surface(X, T, P, cmap='copper', edgecolor='none', alpha=0.8)    #colors = plasma, hot, jet, summer, copper
    ax.set_xlabel('x', fontsize=12);    ax.set_ylabel('t', fontsize=12);    ax.set_zlabel('density', fontsize=12);    ax.set_title(title)

#takes matrix and index between 0 and M
def get_xslice(p, x):
    return  p[:, x]

#takes matrix and index between 0 and N
def get_tslice(p, t):
    return p[t, :]

def get_n_error(approx, exact):
    all_N_errors = []
    for n in range(N):
        N_error = []
        for j in range(M):
            nj_error = abs(exact[n, j] - approx[n, j])
            N_error.append(nj_error)
        all_N_errors.append(dx * (np.sum(N_error)))

    x_2 = np.interp(.2, np.linspace(0,1, N), all_N_errors)      #estimates the point with the given data of all row errors in currrent dx at respeactive time
    x_4 = np.interp(.4, np.linspace(0,1, N), all_N_errors)
    x_6 = np.interp(.6, np.linspace(0,1, N), all_N_errors)
    x_8 = np.interp(.8, np.linspace(0,1, N), all_N_errors)
    x_1 = np.interp(1, np.linspace(0,1, N), all_N_errors)
    return [x_2, x_4, x_6, x_8, x_1]

dx_indexes, dx_UW_error, dx_FUW_error = [],[],[]
for i in range(3,7):
    dx= (1/2)**i
    dt = .8*((2-gamma)/(2+gamma))*dx
    nu = dt/dx
    M,N = int(1/dx) + 1, int(1/dt) + 1

    Upwind_p, filtered_upwind_p, Exact_p = upwind(), filtered_upwind(), Exact()

    dx_indexes.append("dx = {}".format(dx))
    dx_UW_error.append(get_n_error(Upwind_p , Exact_p))
    dx_FUW_error.append(get_n_error(filtered_upwind_p, Exact_p))

error_UW_table = pd.DataFrame(dx_UW_error, columns=["t=.2", "t=.4", "t=.6", "t=.8", "t=1"]);    error_UW_table.index = dx_indexes           #set up the table for excel
error_UW_table.to_excel("upwindErrorTable.xlsx")                                                                                            #export to xlsx format using openpyxl

error_FUW_table = pd.DataFrame(dx_FUW_error, columns=["t=.2", "t=.4", "t=.6", "t=.8", "t=1"]);    error_FUW_table.index = dx_indexes
error_FUW_table.to_excel("FilteredUpwindErrorTable.xlsx")                                                 

#figure 1
fig1 = plt.figure(figsize=plt.figaspect(0.5))                                                       #set up a figure twice as wide as it is tall
f1_ax1 = fig1.add_subplot(1,3,1, projection='3d')                                                   
f1_ax2 = fig1.add_subplot(1,3,2, projection='3d')                                                   
f1_ax3 = fig1.add_subplot(1,3,3, projection='3d')
plot_sol(Upwind_p , f1_ax1, 'Upwind dx = {}, dt = {}'.format(dx, dt))               
plot_sol(filtered_upwind_p, f1_ax2 ,  'Filtered Upwind dx={}, dt={}'.format(dx, dt))
plot_sol(Exact_p, f1_ax3, 'Exact dx={}, dt={}'.format(dx, dt)) 

#figure 2
fig2 = plt.figure(plt.figure(figsize=plt.figaspect(0.5)))
f2_ax1 = fig2.add_subplot(1, 2, 1)
f2_ax1.plot(dx_indexes, error_UW_table["t=1"].tolist())
f2_ax1.set_xlabel('dx', fontsize=12);   f2_ax1.set_ylabel('Error', fontsize=12);    f2_ax1.set_title('error plots at t = 1')

#top right f2
f2_ax2 = fig2.add_subplot(2, 2, 2)
xplots = {"Upwind" : f2_ax2.plot(np.linspace(0, 1, (N)), get_xslice(Upwind_p, int(M/2)))
          ,"Filtered Upwind" : f2_ax2.plot(np.linspace(0, 1, (N)), get_xslice(filtered_upwind_p, int(M/2)))
            ,"Exact" : f2_ax2.plot(np.linspace(0, 1, (N)), get_xslice(Exact_p, int(M/2)))}
plt.legend(xplots);     f2_ax2.set_xlabel('t', fontsize=12);    f2_ax2.set_ylabel('denisity', fontsize=12);     f2_ax2.set_title('slice at t')

#bottom right f2
f2_ax3 = fig2.add_subplot(2, 2, 4)
tplots = {"Upwind" : f2_ax3.plot(np.linspace(0, 1, (M)), get_tslice(Upwind_p, int(N/2)))
          ,"Filtered Upwind" : f2_ax3.plot(np.linspace(0, 1, (M)), get_tslice(filtered_upwind_p, int(N/2)))
            ,"Exact" : f2_ax3.plot(np.linspace(0, 1, (M)), get_tslice(Exact_p, int(N/2)))}
plt.legend(tplots);     f2_ax3.set_xlabel('x', fontsize=12);    f2_ax3.set_ylabel('denisity', fontsize=12);    f2_ax3.set_title('slice at x')

plt.subplots_adjust(wspace=.5, hspace=.8)
plt.show()
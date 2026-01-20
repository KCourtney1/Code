import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parameters
gamma = 1.75
dx = 0.01
dt = 0.8 * dx * ((2 - gamma) / (2 + gamma))
epsilon = 0.5
M = int(1/dx) + 1
N = int(1/dt) + 1

def exact_solution(x, t, epsilon):
    rho = np.zeros_like(x)
    r1 = (x <= 0.5) & (x > t)  # 0 ≤ x ≤ 1/2 and x > t
    r2 = (x <= 0.5) & (x <= t)  # 0 ≤ x ≤ 1/2 and x ≤ t
    rho[r2] = 0.47
    r3 = (x > 0.5) & (t <= (1 / (1 + epsilon) * (x - 0.5) + 0.5))  
    r4 = (x > 0.5) & (t >= (1 / (1 + epsilon) * (x - 0.5) + 0.5))  
    rho[r4] = 0.47
    return rho

# Upwind scheme function
def upwind_scheme(M, N, epsilon=0.5):
    dx = 0.01

    x = np.linspace(0, 1, M-1) 
    t = np.linspace(0, 1, N-1)

    # Velocity
    def velocity(x):
        return 1 if x <= 0.5 else 1 + epsilon

    P = np.zeros((N, M)) 
    P[:, 0] = 0.47  # Boundary condition

    for n in range(N - 1):
        for j in range(1, M):
            v_bar = velocity(j*dx)
            nu = v_bar * dt / dx
            P[n + 1, j] = (1 - nu) * P[n, j] + nu * P[n, j - 1]
    return P, x, t

P, x, t = upwind_scheme(M, N)

# Filtered upwind scheme function
def filtered_upwind_scheme(M, N, epsilon, gamma):
    x = np.linspace(0, 1, M + 1)
    t = np.linspace(0, 1, N + 1)
    dx = 0.01
    dt = 0.8 * ((2 - gamma) / (2 + gamma)) * dx

    P = np.zeros((N + 1, M + 1))
    P[:, 0] = 0.47  # Boundary condition
    
    def velocity(x):
        return 1 if x <= 0.5 else 1 + epsilon
    
        
    for n in range(1, N):
        for j in range(1, M):
            v_bar = velocity(x[j])
            nu = v_bar * (dt / dx)
            P[1, j] = (1 - nu) * P[0, j] + nu * P[0, j - 1]
            # Update using a refined filtered scheme equation
            P[n + 1, j] = ((gamma + (1 - nu) * (1 - (gamma / 2))) * P[n, j]
                           - (gamma / 2) * P[n - 1, j]
                           + nu * (1 - (gamma / 2)) * P[n, j - 1])

    return P, x, t


def error_table(P, x, t, epsilon, t_values=[0.2, 0.4, 0.6, 0.8, 1.0], method="Upwind"):
    errors = []
    print(f"\nError Table for {method} \n" + "-" * 50)
    print(f"{'Time (t)':<10} {'Max Error':<15} {'Average Error':<15}")

    for t_val in t_values:
        t_idx = int(t_val / dt)
        if t_idx >= len(P):
            t_idx = len(P) - 1
        
        approx = P[t_idx, :]
        exact = exact_solution(x, t_val, epsilon)
        error = np.abs(approx - exact)
        max_error = np.max(error)
        avg_error = np.mean(error)
        errors.append([t_val, max_error, avg_error])
        print(f"{t_val:<10.2f} {max_error:<15.5f} {avg_error:<15.5f}")

    error_df = pd.DataFrame(errors, columns=['Time (t)', 'Max Error', 'Average Error'])
    try:
        error_df.to_excel(f'{method}_Error_Table.xlsx', index=False)
        print(f"\n{method} Error Table saved to Excel.")
    except ModuleNotFoundError:
        error_df.to_csv(f'{method}_Error_Table.csv', index=False)
        print(f"openpyxl not found. Saved {method} Error Table as CSV.")

def plot_3d(P_upwind, P, exact, M, N):
    x = np.linspace(0, 1, (M))
    t = np.linspace(0, 1, (N))
    X, T = np.meshgrid(x, t)
    
    fig = plt.figure(figsize=(10, 5))
    
    ax1 = fig.add_subplot(131, projection='3d')
    ax1.plot_surface(X, T, P_upwind, cmap='cool', alpha=0.9)
    ax1.set_xlabel('x')
    ax1.set_ylabel('t')
    ax1.set_zlabel('Density')
    ax1.set_title('Upwind Approximation')
    
    ax2 = fig.add_subplot(132, projection='3d')
    ax2.plot_surface(X, T, P, cmap='cool', alpha=0.9)
    ax2.set_xlabel('x')
    ax2.set_ylabel('t')
    ax2.set_zlabel('Density')
    ax2.set_title('Filtered Upwind Approximation')
    
    ax3 = fig.add_subplot(133, projection='3d')
    ax3.plot_surface(X, T, exact, cmap='cool', alpha=0.9)
    ax3.set_xlabel('x')
    ax3.set_ylabel('t')
    ax3.set_zlabel('Density')
    ax3.set_title('Exact Solution')

    plt.tight_layout()
    plt.show()

P_upwind, x, t = upwind_scheme(M, N, epsilon)
P, x, t = filtered_upwind_scheme(M, N, epsilon, gamma)
exact_solution_grid = np.array([exact_solution(x, t_val, epsilon) for t_val in t])

#error_table(P_upwind, x, t, epsilon, method="Upwind")
#error_table(P, x, t, epsilon, method="Filtered Upwind")

plot_3d(P_upwind, P, exact_solution_grid, M, N)

def plot_x_slices(P_upwind, P, exact_solution_grid, x, t, x_vals=[0.2, 0.5, 0.8]):
    fig, axes = plt.subplots(1, len(x_vals), figsize=(10, 4))  # Adjusted for a single row
    
    for idx, x_val in enumerate(x_vals):
        x_idx = np.abs(x - x_val).argmin()
        
        exact_at_x = exact_solution_grid[:, x_idx]
        upwind_at_x = P_upwind[:, x_idx]
        filtered_at_x = P[:, x_idx]
        
        axes[idx].plot(t, exact_at_x, label="Exact", linestyle='--')
        axes[idx].plot(t, upwind_at_x, label="Upwind Approximation", linestyle=':')
        axes[idx].plot(t, filtered_at_x, label="Filtered Upwind Approximation", linestyle='-.')

        axes[idx].set_title(f"x = {x_val}", fontsize=10)
        axes[idx].set_xlabel("Time (t)", fontsize=9)
        axes[idx].set_ylabel("Density", fontsize=9)
        axes[idx].legend(fontsize=8)
        axes[idx].grid(True)

    plt.tight_layout()
    plt.show()

def plot_t_slices(P_upwind, P, exact_solution_grid, x, t, t_vals=[0.2, 0.5, 0.8]):
    fig, axes = plt.subplots(1, len(t_vals), figsize=(10, 4))  # Adjusted for a single row
    
    for idx, t_val in enumerate(t_vals):
        if t_val < 0 or t_val > np.max(t):
            print(f"Warning: t_val {t_val} is out of bounds. Skipping.")
            continue
        
        t_idx = np.abs(t - t_val).argmin()
        
        exact_at_t = exact_solution_grid[t_idx, :]
        upwind_at_t = P_upwind[t_idx, :]
        filtered_at_t = P[t_idx, :]

        axes[idx].plot(x, exact_at_t, label="Exact", linestyle='--')
        axes[idx].plot(x, upwind_at_t, label="Upwind Approximation", linestyle=':')
        axes[idx].plot(x, filtered_at_t, label="Filtered Upwind Approximation", linestyle='-.')

        axes[idx].set_title(f"t = {t_val}", fontsize=10)
        axes[idx].set_xlabel("Space (x)", fontsize=9)
        axes[idx].set_ylabel("Density", fontsize=9)
        axes[idx].legend(fontsize=8)
        axes[idx].grid(True)

    plt.tight_layout()
    plt.show()

plot_x_slices(P_upwind, P, exact_solution_grid, x, t, x_vals=[0.2, 0.5, 0.8])
plot_t_slices(P_upwind, P, exact_solution_grid, x, t, t_vals=[0.2, 0.5, 0.8])
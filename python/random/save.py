import numpy as np
import pandas as pd

epsilon = 0

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

error_table = []
error_table.append(density_check())
density_error_table = pd.DataFrame(error_table, columns=["dt","True ATT.", 
                                                            "Tolerance ATT. Error", "Tolerance Time Level","Tolerance Est. ATT.",
                                                            "Max ATT. Error", "Max Time Level", "Max Est. ATT."])

def rate_of_convergence(error_table):
    rates = []
    for i in range(1, len(error_table)):
        dx1 = error_table[i-1][0]       #second is position in the table
        dx2 = error_table[i][0]         #use t = 1 and then change gamma
        error1 = error_table[i-1][3] 
        error2 = error_table[i][3]
        rate = np.log(error2 / error1) / np.log(dx2 / dx1)
        rates.append(rate)
    return rates
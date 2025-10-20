import numpy as np
from core.Parametros import L, pi, pwf, eta, delta_p, conversion_factor

def p_mantenimiento(x, t, N=100):
    if t <= 0:
        return pi
    p_steady = pwf + (pi - pwf) * (x / L)
    series_sum = 0
    for n in range(1, N+1):
        term = (2/(n * np.pi)) * delta_p * ((-1)**n) * np.sin(n * np.pi * x / L) * np.exp(-((n * np.pi / L)**2 * eta * t))
        series_sum += term
    return p_steady + series_sum

def q_mantenimiento(t, N=100):
    if t <= 1e-6:
        return conversion_factor * delta_p * 50
    series_sum = sum(np.exp(-((n*np.pi/L)**2)*eta*t) for n in range(1,N+1))
    q = conversion_factor * delta_p * (1 + 2*series_sum)
    return max(q, 100)

def p_impermeable(x, t, N=100):
    if t <= 0:
        return pi
    p = pwf
    for n in range(1,N+1):
        term = (4/((2*n-1)*np.pi))*delta_p*np.sin((2*n-1)*np.pi*x/(2*L))*np.exp(-(((2*n-1)*np.pi/(2*L))**2)*eta*t)
        p += term
    return p

def q_impermeable(t, N=100):
    if t <= 1e-6:
        return conversion_factor*delta_p*30
    series_sum = sum(np.exp(-(((2*n-1)*np.pi/(2*L))**2)*eta*t) for n in range(1,N+1))
    q = 2*conversion_factor*delta_p*series_sum
    return max(q, 50)

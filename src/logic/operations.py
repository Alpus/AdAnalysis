from sympy import diff
from .functions import OneArgFunction
import numpy as np


def solve_cauchy(x0, y0, beta, time, u_func, s_func, z_func, z1_func, step):
    # TODO: make normal realization
    step_count = int(time / step)
    X, Y = np.empty(step_count), np.empty(step_count)
    t = np.arange(0, time, step)
    t[0] = 0
    X[0], Y[0] = x0, y0
    for i in range(1, step_count):
        X[i] = X[i-1] + (t[i] - t[i-1]) * z1_func._calculate(t[i]) * u_func._calculate(Y[i-1])
        Y[i] = Y[i-1] + (t[i] - t[i-1]) * beta * (X[i] - z_func._calculate(t[i]))

    return X, Y, t
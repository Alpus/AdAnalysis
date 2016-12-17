from ..logic.runge_kutta_solver import RungeKuttaSolver
import numpy as np

def test_runge():
	rk = RungeKuttaSolver(
		'-y', 'x', 1, 0,
		args=np.linspace(0, 10, 1000)
	)
	f, g = rk.solve()

	print(f.tabulation, g.tabulation, sep='\n')
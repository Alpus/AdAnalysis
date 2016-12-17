from .functions import OneArgFunction, transformations
from sympy import sympify, Symbol
from sympy.parsing.sympy_parser import parse_expr

class RungeKuttaSolver:
	def __init__(self, f_str, g_str, x0, y0, args):
		self.f = sympify(
			parse_expr(f_str, transformations=transformations)
		)
		self.g = sympify(
			parse_expr(g_str, transformations=transformations)
		)
		self.x0 = x0
		self.y0 = y0
		self.args = args

	def _eval_func(self, func, args):
		return func.evalf(subs=dict(zip(['t', 'x', 'y'], args)))

	def solve(self):
		xs = [self.x0] + [0] * (len(self.args) - 1)
		ys = [self.y0] + [0] * (len(self.args) - 1)
		for i in range(len(self.args) - 1):
			h = self.args[i + 1] - self.args[i]
			t = self.args[i]

			k1_args = t, xs[i], ys[i]
			x_k1 = self._eval_func(self.f, k1_args)
			y_k1 = self._eval_func(self.g, k1_args)

			k2_args = t + h / 2, xs[i] + h / 2 * x_k1, ys[i] + h / 2 * y_k1
			x_k2 = self._eval_func(self.f, k2_args)
			y_k2 = self._eval_func(self.g, k2_args)

			k3_args = t + h / 2, xs[i] + h / 2 * x_k2, ys[i] + h / 2 * y_k2
			x_k3 = self._eval_func(self.f, k3_args)
			y_k3 = self._eval_func(self.g, k3_args)

			k4_args = t + h, xs[i] + h * x_k3, ys[i] + h * y_k3, 
			x_k4 = self._eval_func(self.f, k4_args)
			y_k4 = self._eval_func(self.g, k4_args)

			xs[i + 1] = xs[i] + h / 6 * (x_k1 + 2 * x_k2 + 2 * x_k3 + x_k4)
			ys[i + 1] = ys[i] + h / 6 * (y_k1 + 2 * y_k2 + 2 * y_k3 + y_k4)

		return OneArgFunction(
				arg_vals=list(zip(self.args, xs))
			), OneArgFunction(
				arg_vals=list(zip(self.args, ys))
			)


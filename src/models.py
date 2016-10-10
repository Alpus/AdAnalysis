import os

from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import (
	standard_transformations,
	implicit_multiplication_application,
	function_exponentiation,
	convert_xor,
	factorial_notation,
	auto_symbol,
	auto_number,
	rationalize,
)
from sympy import sympify, Symbol
import numpy as np

import pickle

from .settings import fuctions_save_folder

CURPATH = os.path.dirname(os.path.realpath(__file__))


class Tabulation():
	def is_sorted(self, l):
		return all(l[i] <= l[i+1] for i in range(len(l)-1))

	def __init__(self, args_vals):
		if (len(args) != len(vals)) or (len(set(args)) != len(args)) or not self.is_sorted(args):
			raise Exception('Bad args')

		self.tabulation = zip(args, vals)
		self.begin = args[0]
		self.end = args[len(args) - 1]


class OneArgFunction:
	transformations = (standard_transformations + (
			implicit_multiplication_application,
			function_exponentiation,
			convert_xor,
			factorial_notation,
			rationalize,
		)
	)

	def __init__(self, file=None, tabulation=None, str_func=None, arg=None, begin=None, end=None, step=None):
		if file:
			path = os.path.join(CURPATH, fuctions_save_folder, file)
			self = pickle.load(open(path, 'rb'))
			self.file = file
		elif map(lambda x: x is not None, (str_func, arg, begin, end, step)):
			self.arg = arg
			self.func = sympify(parse_expr(str_func, transformations=self.transformations))
			self.tabulation = self._tabulate(begin, end, step)
		elif tabulation:
			self.tabulation = tabulation
		else:
			raise Exception('Define (file) or (str_func, arg, begin, end, step) or (tabulation)')

	def _calculate(self, val):
		return self.func.evalf(subs={self.arg: val})

	def _tabulate(self, begin, end, step):
		self.tabulation = Tabulation([(arg, self._calculate(arg)) for arg in np.arange(begin, end + step, step)])
		return self.tabulation

	def save_to_file(self, name):
		if hasattr(self, 'name'):
			path = os.path.join(CURPATH, fuctions_save_folder, self.name)
			os.remove(path)

		self.name = name
		path = os.path.join(CURPATH, fuctions_save_folder, self.name)
		pickle.dump(self, open(path, 'w+b'))
		return path

	def delete_from_file(self):
		path = os.path.join(CURPATH, fuctions_save_folder, self.name)
		os.remove(path)
		del self.name
		return path

	def integrate(self):
		if not hasattr(self, 'integral'):
			# TODO: implement normal integrating
			integral_tabulation = Tabulation(*[(arg, 0) for arg in range(self.tabulation.begin, self.tabulation.end, std_step)])
			self.integral = OneArgFunction(tabulation=integral_tabulation)

		return self.integral

	def interpolate(self):
		self.interpolate_coefs = 'FOOBAR'
		return self.interpolate_coefs

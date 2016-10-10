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
)
from sympy import sympify
import pickle

from settings import fuctions_save_folder


class Function:
	def __init__(self, name=None, str_func=None):
		"""
		Get name or str_func. If name is not None load from file else
		create new function.
		"""
		if name:
			path = os.path.join(fuctions_save_folder, name)
			self = pickle.load(open(path, 'rb'))
		elif str_func:
			transformations = (standard_transformations + (
					implicit_multiplication_application,
					function_exponentiation,
					convert_xor,
					factorial_notation,
					auto_number,
				)
			)
			self.func = sympify(parse_expr(str_func, transformations=transformations))
		else:
			raise Exception('Name or str_func must be defined')

	def calculate(self, subs):
		return self.func.evalf(subs=subs)

	def save_to_file(self, name):
		if self.name:
			path = os.path.join(fuctions_save_folder, self.name)
			os.remove(path)

		self.name = name
		path = os.path.join(fuctions_save_folder, self.name)
		pickle.dump(self, open(path, 'wb'))
		return path

	def delete_from_file(self):
		path = os.path.join(fuctions_save_folder, name)
		pickle.dump(self, open(path, 'wb'))
		return path


class OneArgFunction(Function):
	def tabulate(self, arg, begin, end, step):
		self.tabulated = [(x, self.calculate({arg: x})) for x in range(begin, end + step, step)]
		return self.tabulated



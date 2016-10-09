from models import Function, OneArgFunction
from sympy.abc import x

def test_function():
	str_funcs = ['2sin(x)^2', '3x/2 * (cos(x^2) ** 0.2)']
	for str_func in str_funcs:
		try:
			function = OneArgFunction(str_func=str_func)
			print(function)
			print(function.calculate({x: 123.123}))
			print(function.tabulate(arg=x, begin=0, end=1, step=0.01))
			print(function.save_to_file('test'))
			print(function.save_to_file('test2'))
			print(function.delete_from_file())
		except:
			print('FAILED test_function')
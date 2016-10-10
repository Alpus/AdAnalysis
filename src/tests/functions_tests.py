from ..models import Function, OneArgFunction
from sympy.abc import x

def test_function():
	str_funcs = ['2sin(x)^2', '3x/2 * (cos(x^2) ** 0.2)']
	for str_func in str_funcs:
		function = OneArgFunction(str_func=str_func)
		function.calculate({x: 123.123})
		function.tabulate(arg=x, begin=0, end=1, step=0.01)
		function.save_to_file('test')
		function = OneArgFunction(name='test')
		function.save_to_file('test2')
		function.delete_from_file()

	print('OK test_function')
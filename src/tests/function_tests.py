from ..logic.functions import OneArgFunction

def test_function():
	str_funcs = ['2sin(x)^2', 'x^15 - 12^(x/2) + exp(x)']
	for str_func in str_funcs:
		function = OneArgFunction(str_func=str_func, arg='x', begin=0, end=1, points_count=100)
		print(function.save_to_file('test'))
		print(function.tabulation)
		function = OneArgFunction(file='test')
		print(function.tabulation)
		print(function.save_to_file('test2'))
		print(function.file)
		print(function.delete_from_file())

		print(function.interpolate(2000))

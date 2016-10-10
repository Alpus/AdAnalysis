from ..models import OneArgFunction

def test_function():
	str_funcs = ['2sin(x)^2', 'x^15 - 12^(x/2) + exp(x)']
	for str_func in str_funcs:
		function = OneArgFunction(str_func=str_func, arg='x', begin=0, end=1, step=0.01)
		function.save_to_file('test')
		print(function.tabulation)
		function = OneArgFunction(file='test')
		print(function.tabulation)
		function.save_to_file('test2')
		print(function.name)
		function.delete_from_file()
		print(function.name)

	# usecase 1
	p_func = OneArgFunction(str_func='15w * (1 - w)', arg=w, begin=0, end=1, step=0.01)
	p_func.save_to_file('test_p')
	z_func = OneArgFunction(str_func='2sin(t)^2', arg=t, begin=0, end=1, step=0.01)
	z_func.save_to_file('test_z')
	s_func = OneArgFunction(str_func='3t/2 * (cos(t^2) ** 0.2)', arg=t, begin=0, end=1, step=0.01)
	s_func.save_to_file('test_s')

	# usecase 2
	p_func = OneArgFunction(file='test_p')
	p_func.integrate()
	print(p_func.interpolate())

	print('OK test_function')
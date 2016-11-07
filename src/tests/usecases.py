from ..logic.functions import OneArgFunction
from ..logic.operations import solve_cauchy


POINTS_COUNT = 100


def usecase1():
    print('Usecase 1:')
    print('Initializing p_func...')
    p_func = OneArgFunction(str_func='15w * (1 - w)', arg='w', begin=0, end=1, points_count=POINTS_COUNT)
    print('Saved to: ', p_func.save_to_file('test_p'))
    print('Initializing z_func...')
    z_func = OneArgFunction(str_func='2sin(t)^2', arg='t', begin=0, end=1, points_count=POINTS_COUNT)
    print('Saved to: ', z_func.save_to_file('test_z'))
    print('Initializing s_func...')
    s_func = OneArgFunction(str_func='3t/2 * (cos(t^2) ** 0.2)', arg='t', begin=0, end=1, points_count=POINTS_COUNT)
    print('Saved to: ', s_func.save_to_file('test_s'))
    print(p_func.save_to_file('test_p'))
    print(z_func.delete_from_file())
    print(s_func.delete_from_file())


def usecase2():
    p_func = OneArgFunction(file='test_p')
    print(p_func.integrate())
    print(p_func.save_to_file('test_p'))

    print(p_func.delete_from_file())


def usecase3():
    steps_count=100
    u_func = OneArgFunction(str_func='3 * (y ^ 2) - 2 * (y ^ 3)', arg='y', begin=0, end=1, points_count=POINTS_COUNT)
    s_func = OneArgFunction(str_func='3 * t + sin(t)', arg='t', begin=0, end=1, points_count=POINTS_COUNT)
    z_func = OneArgFunction(str_func='4 * t + cos(t)', arg='t', begin=0, end=1, points_count=POINTS_COUNT)
    z1_func = OneArgFunction(str_func='4 - sin(t)', arg='t', begin=0, end=1, points_count=POINTS_COUNT)
    print(
        solve_cauchy(
            x0=0, y0=0, beta=0.01, time=1,
            u_func=u_func, s_func=s_func,
            z_func=z_func, z1_func=z1_func,
            step=0.01
        )
    )

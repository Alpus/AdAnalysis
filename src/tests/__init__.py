#!/usr/local/bin/python3
from .function_tests import test_function
from .usecases import usecase1, usecase2, usecase3
from .linear_systems import test_solver


def test_all():
    test_function()

    usecase1()
    usecase2()
    usecase3()
    
    test_solver()

    print('\n====================')
    print('= OK test_function =')
    print('====================\n')

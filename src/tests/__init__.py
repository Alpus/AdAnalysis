#!/usr/local/bin/python3
from .function_tests import test_function
from .usecases import usecase1, usecase2, usecase3
from .linear_systems import test_solver
from .runge_kutt import test_runge


def test_all():
    test_function()

    usecase1()
    usecase2()
    usecase3()
    
    test_solver()

    test_runge()

    print('\n====================')
    print('= OK test_function =')
    print('====================\n')

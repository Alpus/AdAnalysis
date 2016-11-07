#!/usr/local/bin/python3
from .function_tests import test_function
from .usecases import usecase1, usecase2, usecase3


def test_all():
    test_function()
    usecase1()
    usecase2()
    usecase3()

    print('\n====================')
    print('= OK test_function =')
    print('====================\n')

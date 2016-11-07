import os
from collections import OrderedDict

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

from ..settings import fuctions_save_folder


BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')


class Tabulation:
    def _check_no_repeats(self, list_):
        return(len(list_) != len(set(list_)))

    def __init__(self, args_vals):
        if self._check_no_repeats(list(zip(*args_vals))[0]):
            raise Exception('Repeated args')

        sorted_arg_vals = sorted(args_vals)
        self.tabulation = OrderedDict(sorted_arg_vals)
        self.begin = sorted_arg_vals[0][0]
        self.end = sorted_arg_vals[-1][0]

    def __iter__(self):
        return self.tabulation.__iter__()

    def integrate_trapezoidal(self):
        result = 0
        prev_arg = None
        for arg in self.tabulation:
            if arg > self.begin:
                result += ((self.tabulation[arg] + self.tabulation[prev_arg]) / 2) * (arg - prev_arg)
            prev_arg = arg

        return result


class OneArgFunction:
    transformations = (standard_transformations + (
            implicit_multiplication_application,
            function_exponentiation,
            convert_xor,
            factorial_notation,
            rationalize,
        )
    )

    def __init__(self, file=None, tabulation=None, str_func=None, arg=None, begin=None, end=None, points_count=None):
        if file is not None:
            path = os.path.join(BASE_PATH, fuctions_save_folder, file)
            self.__dict__ = pickle.load(open(path, 'rb')).__dict__
        elif all(map(lambda x: x is not None, (str_func, arg, begin, end, points_count))):
            self.arg = arg
            self.func = sympify(parse_expr(str_func, transformations=self.transformations))
            self.tabulation = self._tabulate(begin, end, points_count)
        elif tabulation is not None:
            self.tabulation = tabulation
        else:
            raise Exception('Define (file) or (str_func, arg, begin, end, step) or (tabulation)')

    def _calculate(self, val):
        return self.func.evalf(subs={self.arg: val})

    def _tabulate(self, begin, end, points_count):
        self.tabulation = Tabulation([(arg, self._calculate(arg)) for arg in np.linspace(begin, end, points_count)])
        return self.tabulation

    def save_to_file(self, file):
        if hasattr(self, 'file'):
            path = os.path.join(BASE_PATH, fuctions_save_folder, self.file)
            os.remove(path)

        self.file = file
        path = os.path.join(BASE_PATH, fuctions_save_folder, self.file)
        pickle.dump(self, open(path, 'w+b'))
        return path

    def delete_from_file(self):
        path = os.path.join(BASE_PATH, fuctions_save_folder, self.file)
        os.remove(path)
        del self.file
        return path

    def integrate(self):
        # if not hasattr(self, 'integral') or self.integral.method != lower(method):
        #     if method not in self.tabulation.integration_methods:
        #         raise ValueError(
        #             'There are no method {user_method}, choose one from: {methods}'.format(
        #                     user_method=method,
        #                     methods=Tabulation.integration_methods
        #                 )
        #             )
        self.integral = self.tabulation.integrate_trapezoidal()

        return self.integral

    def interpolate(self):
        self.interpolate_coefs = 'FOOBAR'
        return self.interpolate_coefs

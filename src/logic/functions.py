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
    rationalize,
)
from sympy import sympify, Symbol
import numpy as np

import pickle

from ..settings import fuctions_save_folder

BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')


class Tabulation:
    def is_args_sorted(self, args_vals):
        return all(args_vals[i][0] <= args_vals[i+1][0] for i in range(len(args_vals)-1))

    def __init__(self, args_vals):
        if not self.is_args_sorted(args_vals):
            raise Exception('Bad args')

        self.tabulation = args_vals
        self.begin = args_vals[0][0]
        self.end = args_vals[len(args_vals) - 1][0]

    def __iter__(self):
        return self.tabulation.__iter__()


class OneArgFunction:
    transformations = (standard_transformations + (
            implicit_multiplication_application,
            function_exponentiation,
            convert_xor,
            factorial_notation,
            rationalize,
        )
    )

    def __init__(self, file=None, tabulation=None, str_func=None, arg=None, begin=None, end=None, step=None):
        if file is not None:
            path = os.path.join(BASE_PATH, fuctions_save_folder, file)
            self.__dict__ = pickle.load(open(path, 'rb')).__dict__
        elif all(map(lambda x: x is not None, (str_func, arg, begin, end, step))):
            self.arg = arg
            self.func = sympify(parse_expr(str_func, transformations=self.transformations))
            self.tabulation = self._tabulate(begin, end, step)
        elif tabulation is not None:
            self.tabulation = tabulation
        else:
            raise Exception('Define (file) or (str_func, arg, begin, end, step) or (tabulation)')

    def _calculate(self, val):
        return self.func.evalf(subs={self.arg: val})

    def _tabulate(self, begin, end, step):
        self.tabulation = Tabulation([(arg, self._calculate(arg)) for arg in np.arange(begin, end + step, step)])
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
        if not hasattr(self, 'integral'):
            # TODO: implement normal integrating
            integral_tabulation = Tabulation([(arg, 0) for arg, val in self.tabulation])
            self.integral = OneArgFunction(tabulation=integral_tabulation)

        return self.integral

    def interpolate(self):
        self.interpolate_coefs = 'FOOBAR'
        return self.interpolate_coefs

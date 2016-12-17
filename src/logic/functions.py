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

from .linear_systems import LinearSystemsSolver
from ..settings import fuctions_save_folder


BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
transformations = (standard_transformations + (
            implicit_multiplication_application,
            function_exponentiation,
            convert_xor,
            factorial_notation,
            rationalize,
        )
    )

class OneArgFunction:
    def __init__(self, file=None, arg_vals=None, str_func=None, arg=None, begin=None, end=None, points_count=None):
        if file is not None:
            path = os.path.join(BASE_PATH, fuctions_save_folder, file)
            self.__dict__ = pickle.load(open(path, 'rb')).__dict__
        elif all(map(lambda x: x is not None, (str_func, arg, begin, end, points_count))):
            self.begin = begin
            self.end = end
            self.step = (end - begin) / points_count

            self.arg = arg
            self.func = sympify(parse_expr(str_func, transformations=transformations))
            self.tabulation = self._tabulate(begin, end, points_count)
        elif arg_vals is not None:
            self.tabulation = self._make_tabulation_from_arg_vals(arg_vals)
            self.step = list(self.tabulation.keys())[1] - list(self.tabulation.keys())[0]
        else:
            raise Exception('Define (file) or (str_func, arg, begin, end, step) or (tabulation)')

    # Tabulation
    def _tabulate(self, begin, end, points_count):
        self.tabulation = self._make_tabulation_from_arg_vals(
            [
                (
                    arg, self._calculate(arg)) for arg in np.linspace(
                        begin, end, points_count
                )
            ]
        )
        return self.tabulation

    def _check_no_repeats(self, list_):
        return(len(list_) != len(set(list_)))

    def _make_tabulation_from_arg_vals(self, arg_vals):
        if self._check_no_repeats(list(zip(*arg_vals))[0]):
            raise Exception('Repeated args')

        sorted_arg_vals = sorted(arg_vals)
        self.tabulation = OrderedDict(sorted_arg_vals)
        self.begin = sorted_arg_vals[0][0]
        self.end = sorted_arg_vals[-1][0]

        return self.tabulation

    # Caclulation of function
    def _calculate(self, val):
        return self.func.evalf(subs={self.arg: val})

    # Work with file
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

    # Integrating
    def integrate_trapezoidal(self):
        result = 0
        prev_arg = None
        for arg in self.tabulation:
            if arg > self.begin:
                result += ((self.tabulation[arg] + self.tabulation[prev_arg]) / 2) * (arg - prev_arg)
            prev_arg = arg

        return result

    def integrate(self):
        self.integral = self.integrate_trapezoidal()
        return self.integral

    # Interpolation
    def _get_interpolate_coefs(self):
        tabilation_args = list(self.tabulation.keys())
        tabilation_values = list(self.tabulation.values())
        self.spline_coefs = [dict() for arg in range(len(tabilation_values))]

        matrix = [[0] * (len(tabilation_values) - 1) for x in range(len(tabilation_values) - 2)]
        for num in range(len(tabilation_values) - 2):
            f_prev = tabilation_values[num]
            f = tabilation_values[num + 1]
            f_next = tabilation_values[num + 2]
            h = tabilation_args[num + 1] - tabilation_args[num]
            h_next = tabilation_args[num + 2] - tabilation_args[num + 1]
            matrix[num][num - 1] = h
            matrix[num][num] = 2 * (h + h_next)
            matrix[num][num + 1] = h_next
            matrix[num][-1] = 6 * ((f_next - f) / h_next - (f - f_prev) / h)

        l_solver = LinearSystemsSolver(matrix)
        c = l_solver.get_solution()

        for num in range(len(self.spline_coefs)):
            if num == 0 or num == len(self.spline_coefs) - 1:
                self.spline_coefs[num]['c'] = 0
            else:
                self.spline_coefs[num]['c'] = c[num - 1]

        for num, (arg, val) in enumerate(self.tabulation.items()):
            if num - 1 == len(self.tabulation):
                break

            self.spline_coefs[num]['a'] = val

            if num == 0:
                self.spline_coefs[num]['d'] = 0
                self.spline_coefs[num]['b'] = 0
            else:
                self.spline_coefs[num]['d'] =\
                    (self.spline_coefs[num]['c'] - self.spline_coefs[num - 1]['c']) / self.step

                f = val
                f_prev = tabilation_values[num - 1]
                h = tabilation_args[num] - tabilation_args[num - 1]
                c = self.spline_coefs[num]['c']
                c_prev = self.spline_coefs[num - 1]['c']

                self.spline_coefs[num]['b'] = (f - f_prev) / h + h * (2 * c + c_prev) / 6

        return self.spline_coefs

    def interpolate_point(self, point):
        if not hasattr(self, 'spline_coefs'):
            self._get_interpolate_coefs()
        
        tabulation_args = list(self.tabulation.keys())
        cur_tab_num = 0

        result = OrderedDict()

        while cur_tab_num <= len(self.tabulation):
            if point < tabulation_args[cur_tab_num]:
                a_b_c_d = self.spline_coefs[cur_tab_num]
                a, b, c, d, x, x_i = a_b_c_d['a'], a_b_c_d['b'], a_b_c_d['c'], a_b_c_d['d'],\
                                    point, tabulation_args[cur_tab_num]
                return a + b * (x - x_i) + (c / 2) * ((x - x_i) ** 2) +\
                            d / 6 * ((x - x_i) ** 3)

            cur_tab_num += 1

    def interpolate(self, points_count):
        if not hasattr(self, 'spline_coefs'):
            self._get_interpolate_coefs()

        interpolate_step = (self.end - self.begin) / (points_count)
        
        tabulation_args = list(self.tabulation.keys())
        cur_point = self.begin
        cur_tab_num = 1

        result = OrderedDict()

        while cur_tab_num < len(self.tabulation):
            a_b_c_d = self.spline_coefs[cur_tab_num]
            a, b, c, d, x, x_i = a_b_c_d['a'], a_b_c_d['b'], a_b_c_d['c'], a_b_c_d['d'],\
                                cur_point, tabulation_args[cur_tab_num]
            result[cur_point] = a + b * (x - x_i) + (c / 2) * ((x - x_i) ** 2) +\
                                    d / 6 * ((x - x_i) ** 3)

            cur_point += interpolate_step
            if cur_point > tabulation_args[cur_tab_num]:
                cur_tab_num += 1

        return result





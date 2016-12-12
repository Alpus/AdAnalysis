import numpy as np


class LinearSystemsSolver:
    """
    Tomas algorithm
    """
    def __init__(self, coefs_matrix):
        # Make np.ndarray
        self._coefs_matrix = np.array(coefs_matrix).astype(float)

        # First check of solution existance
        self._height = self._coefs_matrix.shape[0]
        self._width = self._coefs_matrix.shape[1]

        if self._height != self._width - 1:
            raise ValueError('Bad matrix shape')

        self._d = self._coefs_matrix[:,self._width - 1]

        self._a_b_g = np.zeros((self._height, 3))
        for row_num, row in enumerate(self._coefs_matrix[:, 0:-1]):
            begin_col = max(row_num - 1, 0)
            end_col = min(row_num + 2, self._width)

            if any(row[0:begin_col]) or any(row[end_col:self._width]):
                raise ValueError('Not tridiagonal matrix')

            if row_num == 0:
                self._a_b_g[row_num] = [0.0] + list(row[begin_col:end_col])
            elif row_num == self._height - 1:
                self._a_b_g[row_num] =  list(row[begin_col:end_col]) + [0.0]
            else:
                self._a_b_g[row_num] = row[begin_col:end_col]

            self._a_b_g[row_num][1] = - self._a_b_g[row_num][1]

    def _forward_move(self):
        self._p = np.zeros((self._height, 1))
        self._q = np.zeros((self._height, 1))
        for row_number, ((a, b, g), d) in enumerate(zip(self._a_b_g, self._d)):
            if a == 0:
                self._p[row_number] = g / b
                self._q[row_number] = - d / b
            else:
                self._p[row_number] = g / (b - a * self._p[row_number - 1])
                self._q[row_number] = (a * self._q[row_number - 1] - d) / (b - a * self._p[row_number - 1])

    def _backward_move(self):
        self._x = np.zeros(self._height)
        n = self._height - 1
        a_n, b_n, g_n = self._a_b_g[n]
        self._x[n] = (a_n * self._q[n - 1] - self._d[n]) / (b_n - a_n * self._p[n - 1]) 
        for r_row_num, row in enumerate(self._coefs_matrix[::-1]):
            row_num = self._height - r_row_num - 1
            if row_num == 0:
                break
            self._x[row_num - 1] = self._p[row_num - 1] * self._x[row_num] + self._q[row_num - 1]


    def get_solution(self):
        self._forward_move()
        self._backward_move()
        return self._x

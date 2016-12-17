from ..logic.linear_systems import LinearSystemsSolver
import numpy as np


def test_sample(sample_linear_system, correct_answer):
    print('Linear System:', sample_linear_system, sep='\n')
    print('Correct answer:', correct_answer, sep='\n')

    solver = LinearSystemsSolver(sample_linear_system)
    answer = list(solver.get_solution())

    print('Real answer:', answer, sep='\n')

    for f, s in zip(correct_answer, answer):
        if abs(f - s) > 1e-5:
            raise ValueError('Answer is not correct')
    else:
        print('Answer is correct!\n')


def test_solver():
    sample_linear_system_1 = np.array(
        [
            [-1, 1, 0, 6],
            [0, 1, 1, 3],
            [0, 0, 1, 2],
        ]
    )
    correct_answer_1 = [-5, 1, 2]
    test_sample(sample_linear_system_1, correct_answer_1)

    sample_linear_system_2 = np.array(
        [
            [-1, 4, 0, 0, 6],
            [0, 4, 1, 0, 3],
            [0, 0, 7, 1, 9],
            [0, 0, 0, 6, 12],
        ]
    )
    correct_answer_2 = [-4, 0.5, 1, 2]
    test_sample(sample_linear_system_2, correct_answer_2)

    sample_linear_system_3 = np.array(
        [
            [2, 1, 0, 0, 6],
            [1, 2, 1, 0, 3],
            [0, 1, 5, -2, 11],
            [0, 0, -2, 7, 1],
        ]
    )
    correct_answer_3 = [4, -2, 3, 1]
    test_sample(sample_linear_system_3, correct_answer_3)

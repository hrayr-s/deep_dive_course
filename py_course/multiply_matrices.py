import random
from concurrent.futures import ThreadPoolExecutor

import numpy as np

from print_funcs import print_side_by_side


def multiply_rows(Ai, Bi):
    return [Ai[i] * Bi[i] for i, _ in enumerate(Ai)]


def print_matrix(Ai, Bi):
    print(multiply_rows(Ai, Bi))


def multiply_matrices(A, B):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = []
        for _rows in zip(A, B):
            results.append(executor.submit(multiply_rows, _rows[0], _rows[1]))

        new_matrix = list(result.result() for result in results)
        print_side_by_side([A, B, new_matrix])


if __name__ == '__main__':

    rows, cols = 3, 4

    # Integers from 0 to 9
    random_int_matrix1 = np.random.randint(0, 10, size=(rows, cols))
    random_int_matrix2 = np.random.randint(0, 10, size=(rows, cols))


    # Generate random matrix with integers 0 to 9
    random_matrix1 = list(
        list(random.randint(0, 9) for _ in range(cols))
        for _ in range(rows)
    )

    # Generate random matrix with integers 0 to 9
    random_matrix2 = list(
        list(random.randint(0, 9) for _ in range(cols))
        for _ in range(rows)
    )

    multiply_matrices(random_matrix1, random_matrix2)

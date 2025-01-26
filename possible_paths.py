import random
from typing import List

from print_funcs import print_side_by_side, pr_red, pr_purple, pr_cyan


def walk_on_matrix(matrix: List[List[int]]) -> int:
    if matrix[-1][-1] == 1:
        raise Exception('Cannot reach')

    tmp_matrix = []
    for row in matrix:
        tmp_matrix.append([0 for _ in range(len(row))])

    tmp_matrix[-1][-1] = 1

    i = len(matrix) - 2
    j = len(matrix[0]) - 2

    while i > 0:
        if matrix[-1][i+1] == 0 and tmp_matrix[-1][i+1] == 1:
            tmp_matrix[-1][i] += tmp_matrix[-1][i+1]
        else:
            tmp_matrix[-1][i] = 0
        i -= 1

    while j > 0:
        if matrix[j+1][-1] == 0 and tmp_matrix[j+1][-1] == 1:
            tmp_matrix[j][-1] = 1
        else:
            tmp_matrix[j][-1] = 0

        j -= 1

    i = len(matrix) - 2
    j = len(matrix[0]) - 2

    while i >= 0:
        j = len(matrix[i]) - 2
        while j >= 0:
            if matrix[i][j] == 0:
                tmp_matrix[i][j] += tmp_matrix[i][j + 1]
            if matrix[i][j] == 0:
                tmp_matrix[i][j] += tmp_matrix[i+1][j]
            j -= 1
        i -= 1

    print_side_by_side([matrix, tmp_matrix], conditional_print=lambda x: x > 0 and pr_cyan or print)

    return tmp_matrix[0][0]

def main(array: list) -> None:
    """
    Calculate the count of possible walking paths in matrix.
    :param array:
    :return:
    """
    pass

if __name__ == "__main__":
    some_array = [
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
    ]

    m = 0
    could_not_generate = 0
    while m == 0:
        try:
            some_array = [[(random.randint(0, 10) * 89) % 2 for i in range(10)] for _ in range(10)]
            pr_cyan("=" * 30)
            pr_purple(f"Trial #{could_not_generate+1}")
            pr_cyan("=" * 30)
            m = walk_on_matrix(some_array)
            pr_red(m)
            if m == 0:
                could_not_generate = could_not_generate + 1
            else:
                could_not_generate = 0
        except Exception:
            could_not_generate += 1
            pr_red(could_not_generate, end="\r")


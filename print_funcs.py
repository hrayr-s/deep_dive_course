import typing
from typing import List, Callable, Any


def pr_red(skk, end='\n'): print("\033[91m {}\033[00m".format(skk), end=end)


def pr_green(skk, end='\n'): print("\033[92m {}\033[00m".format(skk), end=end)


def pr_yellow(skk, end='\n'): print("\033[93m {}\033[00m".format(skk), end=end)


def pr_light_purple(skk, end='\n'): print("\033[94m {}\033[00m".format(skk), end=end)


def pr_purple(skk, end='\n'): print("\033[95m {}\033[00m".format(skk), end=end)


def pr_cyan(skk, end='\n'): print("\033[96m {}\033[00m".format(skk), end=end)


def pr_light_gray(skk, end='\n'): print("\033[97m {}\033[00m".format(skk), end=end)


def pr_black(skk, end='\n'): print("\033[98m {}\033[00m".format(skk), end=end)


def print_matrix(matrix: List[List[int]]) -> None:
    for row in matrix:
        print(row)


def print_side_by_side(
        matrix_list: List[List[List[int]]],
        row_prefixes: List[List[str]] = None,
        col_prefixes: List[List[str]] = None,
        conditional_print: typing.Callable[[Any], Callable] = lambda _: print,
) -> None:
    assert row_prefixes is None or all(len(row_prefixes[i]) == len(mat) for i, mat in enumerate(matrix_list))
    assert col_prefixes is None or all(len(col_prefixes[i]) == len(mat[0]) for i, mat in enumerate(matrix_list))

    if col_prefixes is not None:
        for i, col_prefix_list in enumerate(col_prefixes):
            print(' ', end='\t')
            pr_red('\t'.join(col_prefix_list), end='')
            print('', end="\t\t\t|\t\t")

        print('')

    for i in range(len(matrix_list[0])):
        # we go over rows
        for m in range(len(matrix_list)):
            if row_prefixes is not None:
                pr_red(row_prefixes[m][i], end="\t")
            for j in range(len(matrix_list[m][i])):
                conditional_print(matrix_list[m][i][j])(matrix_list[m][i][j], end="\t")
            print("\t\t", end="|\t\t")
        print("")

from typing import Tuple, List

from print_funcs import print_matrix, print_side_by_side


class Knapsack:
    def __init__(self, W: int, items: List[Tuple[int, int]]) -> None:
        self.W = W
        self.items = [(0, 0)] + items
        self.m = [[-1 for j in range(self.W)] for i in range(len(self.items))]
        for i in range(self.W):
            self.m[0][i] = 0
        for i in range(1, len(self.items)):
            self.m[i][0] = 0

    def max_profit(self) -> int:
        for i in range(1, len(self.items)):
            for j in range(1, self.W):
                if self.items[i][0] > j:  # weight of item is greater than current calculating weight in loop
                    self.m[i][j] = self.m[i - 1][j]
                else:
                    self.m[i][j] = max(self.m[i - 1][j], self.m[i - 1][j - self.items[i][0]] + self.items[i][1])
        return self.m[-1][-1]

    def print_calculated_matrix(self) -> None:
        print_side_by_side([self.m])


if __name__ == '__main__':
    # W_items = [(3, 3), (2, 1), (5, 2)]
    W_items = [(2, 1), (5, 2), (3, 3), (4, 4), (7, 5)]
    W = 10
    knapsack = Knapsack(W, W_items)
    print(knapsack.max_profit())
    knapsack.print_calculated_matrix()

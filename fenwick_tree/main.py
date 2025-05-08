import random
from typing import List, Any, Callable


class FenwickTree:

    def __init__(self, array: List[Any], aggregation_method: Callable[[Any, Any], Any]) -> None:
        self.array = [array]
        self.meth = aggregation_method
        self._calc_levels()

    def _calc_levels(self):
        level = 0
        while len(self.array[level]) > 1:
            next_level = level + 1
            if len(self.array) < (next_level + 1):
                self.array.append([])
            for i in range(0, len(self.array[level]), 2):
                b = None
                if len(self.array[level]) > (i + 1):
                    b = self.array[level][i + 1]
                self.array[next_level].append(
                    self.meth(
                        self.array[level][i],
                        b,
                    )
                )
            level += 1

    def aggr(self, start: int, end: int) -> Any:
        assert 0 <= start < len(self.array[0])
        assert start < end
        temp_aggr_result = None
        level = 0
        # while len(self.array[level][start:end]) > 1:
        while start < end:
            if end >= len(self.array[level]):
                end = len(self.array[level]) - 1

            if start % 2 == 1:
                start += 1
                temp_aggr_result = self.meth(self.array[level][start], temp_aggr_result)
            start = start // 2

            if end % 2 == 1:
                end -= 1
                temp_aggr_result = self.meth(self.array[level][end], temp_aggr_result)

            end = end // 2

            level += 1
        return self.meth(self.array[level][start], temp_aggr_result)

def ppprint(array: List[List[Any]]) -> True:
    for j, arr in enumerate(array):
        print('\t' * j, arr)

    return True

if __name__ == "__main__":
    for k in range(1000):
        arr = [random.randint(1, 40) for _ in range(20)]
        g_start = random.randint(0, len(arr) - 3)
        g_end = random.randint(g_start+1, len(arr) - 1)
        fenwick_tree = FenwickTree(arr, lambda a, b: b and a < b and b or a)
        fnwk = fenwick_tree.aggr(g_start, g_end)
        max_m = max(arr[g_start:g_end])
        assert fnwk == max_m, ppprint(fenwick_tree.array) and f"start: {g_start} & end: {g_end}; {fnwk} != {max_m}"

    # arr = [random.randint(1, 40) for _ in range(20)]
    # arr = [7, 27, 4, 15, 15, 2, 40, 18, 27, 39, 5, 1, 37, 4, 28, 30, 14, 22, 79, 9]
    # arr = [27, 29, 21, 9, 5, 29, 33, 3, 22, 12, 32, 34, 13, 19, 21, 14, 26, 18, 2, 23]
    # start = 14
    # end = 18

    # fenwick = FenwickTree(arr, lambda a, b: b and a < b and b or a)
    # for j, arr in enumerate(fenwick.array):
    #     print('\t' * j, arr)

    # print(fenwick.aggr(6, 18))
    # print(fenwick.aggr(start, end))

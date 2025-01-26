"""
Longest Common Subsequence (LCS)
"""
from print_funcs import print_side_by_side, pr_light_gray, pr_light_purple, pr_yellow


class LongestCommonSubsequence:
    def __init__(self, string1, string2):
        self.string1 = " " + string1
        self.string2 = " " + string2
        self.matrix = [
            [
                -1 for x in range(len(self.string2))
            ]
            for x in range(len(self.string1))
        ]
        for i1 in range(len(self.string1)):
            self.matrix[i1][0] = 0
        for i2 in range(len(self.string2)):
            self.matrix[0][i2] = 0

    def lcs(self, i1, i2):
        if i1 <= 0 or i2 <= 0:
            return 0

        if self.string1[i1] == self.string2[i2]:
            self.matrix[i1][i2] = self.lcs(i1 - 1, i2 - 1) + 1
        else:
            self.matrix[i1][i2] = max(self.lcs(i1 - 1, i2), self.lcs(i1, i2 - 1))

        return self.matrix[i1][i2]

    @staticmethod
    def conditional_print(n):
        return n < 0 and pr_yellow or print

    def calc_lcs(self):
        self.lcs(len(self.string1) - 1, len(self.string2) - 1)
        print_side_by_side(
            [self.matrix],
            row_prefixes=[self.string1],
            col_prefixes=[self.string2],
            conditional_print=self.conditional_print
        )
        return self.matrix[-1][-1]

    def usage_percentage(self):
        used = 0
        for row in self.matrix:
            for cell in row:
                if cell >= 0:
                    used += 1

        return (used / (len(self.matrix) * len(self.matrix[0]))) * 100


def calc_lcs(string1, string2):
    s1 = " " + string1
    s2 = " " + string2
    a_b_matrix = [[0] * (len(s1))]
    a_b_matrix[0] = [0 for _ in range(len(s2))]
    for i in range(1, len(s1)):
        a_b_matrix.append([-1 for i in range(len(s2))])
        a_b_matrix[i][0] = 0

    print_side_by_side([a_b_matrix])

    for i in range(1, len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                a_b_matrix[i][j] = a_b_matrix[i - 1][j - 1] + 1
            else:
                a_b_matrix[i][j] = max(a_b_matrix[i - 1][j], a_b_matrix[i][j - 1])
    print_side_by_side(
        [a_b_matrix],
        row_prefixes=[s1],
        col_prefixes=[s2],
        conditional_print=LongestCommonSubsequence.conditional_print
    )
    return a_b_matrix[-1][-1]


if __name__ == "__main__":
    if input("Test or try:").lower() != "test":
        str1 = input("Enter the first string: ")
        str2 = input("Enter the second string: ")
    else:
        str1 = "acatgt" * 2
        str2 = "ctgaat" * 2
        # str1 = 'aaaabbbb'
        # str2 = 'bbbbcccc'

    print("Longest Common Subsequence (LCS) using DP:")
    calc_lcs(str1, str2)

    print("Longest Common Subsequence (LCS) using Memoization:")
    lcs = LongestCommonSubsequence(str1, str2)
    lcs.calc_lcs()
    print(f"used percentage: {lcs.usage_percentage()}")

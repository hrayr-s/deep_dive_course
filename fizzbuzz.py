import re
from typing import List, Union

pair_conditions = [
    (lambda n: n % 3 == 0, 'Fizz'),
    (lambda n: n % 5 == 0, 'Buzz'),
]


def fizzbuzz_with_int(data: List[Union[int, str]]):
    """
    FizzBuzz with normal integers list and operations.
    Any type of data other than integers are skipped.
    :param data:
    :return:
    """
    results = []
    for number in data:
        if not isinstance(number, int):
            continue

        _result = ''
        for condition, printable_string in pair_conditions:
            if condition(number):
                _result += printable_string
        results.append(_result)
    return results


str_conditions = [
    (lambda n: n[-1] in '369', 'Fizz'),
    (lambda n: n[-1] in '05', 'Buzz'),
]


def fizzbuzz(data: List[str]):
    """
    Hardcore FizzBuzz with the following rules:
        - no integers, input includes strings only
        - each string can represent a number or may not
        - the data includes letters, symbols, digits that can be types from keyboard by one press only
        -
    :param data:
    :return:
    """
    results = []
    for number in data:
        if not re.match(r'^[0-9]+$', number):
            continue
        results.append(''.join([pr_str for condition, pr_str in str_conditions if condition(number)]))

    return results


if __name__ == '__main__':
    result_me = []
    for i in range(10000):
        if i % 13:
            r1 = fizzbuzz(['sakd0'])
            r2 = fizzbuzz_with_int(['sakd0'])
            result_me.append((r1 and r1[0] or '', r2 and r2[0] or ''))
        r1 = fizzbuzz([str(i)])
        r2 = fizzbuzz_with_int([i])
        result_me.append((r1[0],r2[0]))

    for r1, r2 in result_me:
        if r1 != r2:
            print(r1)
            print(r2)
        # else:
        #     print(r1)

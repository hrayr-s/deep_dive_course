# fibonacci sequence
# check odd
# generates index

def fibonacci():
    a = 0
    b = 1

    while True:
        yield a
        a, b = b, a + b


def is_odd(sequence):
    for element in sequence:
        if element % 2 == 0:
            yield element


def add_index(sequence):
    i = 0
    for element in sequence:
        yield i, element
        i += 1


if __name__ == '__main__':
    c = fibonacci()
    print(next(c))
    print(next(c))
    for _ in range(10):
        print(next(c))

    odds = is_odd(c)

    for _ in range(10):
        print(next(odds))

    indexed = add_index(odds)

    for _ in range(10):
        print(next(indexed))

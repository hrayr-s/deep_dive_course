
_possible_set = []
_w_weight_map = []

def fill_rucksack(width, items, _bonus):
    if width == 0:
        return 0
    if width < 0:
        return -9999999999

    _possible_set.append(width)
    _calc_list = []

    for w, bonus in items:
        _calc_list.append((w, fill_rucksack(width - w, items, _bonus) + bonus))
    # _calc_list = list((w, fill_rucksack(width - w, items) + bonus) for w, bonus in items)

    calculated = max(_i for _, _i in _calc_list)
    _w_weight_map.append((width, calculated, _calc_list))
    return calculated


if __name__ == '__main__':
    # W_items = [(2, 1), (5, 2), (3, 3)]
    W_items = [(2, 1), (5, 2), (3, 3), (4, 4), (7, 5)]
    W = 10
    print(fill_rucksack(W, W_items, 0))
    for i in _w_weight_map:
        print(i)

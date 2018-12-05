"""
https://adventofcode.com/2018/day/2
"""
from typing import Dict


def get_symbol_map(box_id: str) -> Dict[str, int]:
    """
    Calculates symbol map for the given uid.
    """
    result = {}
    for symbol in box_id:
        try:
            result[symbol] += 1
        except KeyError:
            result[symbol] = 1
    return result


with open("./input.txt") as f:
    box_ids = f.read().splitlines()
    count_having_2 = 0
    count_having_3 = 0

    for box_id in box_ids:
        counts = set(get_symbol_map(box_id).values())
        if 2 in counts:
            count_having_2 += 1
        if 3 in counts:
            count_having_3 += 1

    print(count_having_2 * count_having_3)

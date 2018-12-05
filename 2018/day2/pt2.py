"""
https://adventofcode.com/2018/day/2
"""
from typing import Tuple


def get_diff_count(box_id1: str, box_id2: str) -> Tuple[int, str]:
    """
    Calculates amount of different symbols for two strings.
    """
    count = 0
    common = ""
    for i in range(len(box_id1)):
        if box_id1[i] != box_id2[i]:
            count += 1
        else:
            common += box_id1[i]

    return count, common


with open("./input.txt") as f:
    box_ids = f.read().splitlines()

    for box_id1 in box_ids:
        for box_id2 in box_ids:
            count, common = get_diff_count(box_id1, box_id2)
            if count == 1:
                print(f'common: {common}')

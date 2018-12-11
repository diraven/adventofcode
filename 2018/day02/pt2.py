"""
https://adventofcode.com/2018/day/2

--- Part Two ---

Confident that your list of box IDs is complete, you're ready to find the boxes full of prototype fabric.

The boxes will have IDs which differ by exactly one character at the same position in both strings. For example, given the following box IDs:

abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz

The IDs abcde and axcye are close, but they differ by two characters (the second and fourth). However, the IDs fghij and fguij differ by exactly one character, the third (h and u). Those must be the correct boxes.

What letters are common between the two correct box IDs? (In the example above, this is found by removing the differing character from either ID, producing fgij.)
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

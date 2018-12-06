"""
https://adventofcode.com/2018/day/3

--- Part Two ---

Amidst the chaos, you notice that exactly one claim doesn't overlap by even a single square inch of fabric with any other claim. If you can somehow draw attention to it, maybe the Elves will be able to make Santa's suit after all!

For example, in the claims above, only claim 3 is intact after all claims are made.

What is the ID of the only claim that doesn't overlap?
"""

import timeit
from typing import Tuple, List


def check_claim(
        heat_map: List[List[int]],
        claim: Tuple[int, int, int, int, int]
) -> bool:
    """
    Checks if given claim is clean.
    """
    for x in range(int(claim[1]), int(claim[1]) + int(claim[3])):
        for y in range(int(claim[2]), int(claim[2]) + int(claim[4])):
            if heat_map[x][y] > 1:
                return False
    return True


def run() -> None:
    """
    Main function.
    """
    heat_map = [[0 for x in range(1000)] for x in range(1000)]

    with open("./input.txt") as f:
        claims = []  # type: List[Tuple[int, int, int, int, int]]

        # Original format: 1 @ 335,861: 14x10
        # Parsed format: (
        # 0: id,
        # 1: origin_x,
        # 2: origin_y,
        # 3: size_x,
        # 4: size_y
        # )
        for line in f.read().splitlines():
            id_origin_size = line.split('@')
            ident = id_origin_size[0].lstrip('#')
            origin_size = id_origin_size[1].strip().split(': ')
            origin = origin_size[0].split(',')
            size = origin_size[1].split('x')
            claims.append((int(ident), int(origin[0]), int(origin[1]),
                           int(size[0]), int(size[1])))

        # Fill out the heatmap.
        for claim in claims:
            for x in range(int(claim[1]), int(claim[1]) + int(claim[3])):
                for y in range(int(claim[2]), int(claim[2]) + int(claim[4])):
                    heat_map[x][y] += 1

        # Now check which claim is not heated.
        for claim in claims:
            if check_claim(heat_map, claim):
                print(claim)


print(timeit.timeit(run, number=1))

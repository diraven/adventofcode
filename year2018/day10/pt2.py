"""
--- Part Two ---

Good thing you didn't have to wait, because that would have taken a long time - much longer than the 3 seconds in the example above.

Impressed by your sub-hour communication capabilities, the Elves are curious: exactly how many seconds would they have needed to wait for that message to appear?
"""
import copy
import re
import timeit
from typing import List, Tuple

Circle = List[int]


def run() -> None:
    """
    Main function.
    """
    # with open("./input.example.txt") as f:
    with open("./input.txt") as f:
        rexp = re.compile(
            r"position=<\s*([-0-9]+),\s+([-0-9]+)>\s+"
            r"velocity=<\s?([-0-9]+),\s+([-0-9]+)>"
        )

        points = []  # type: List[List[Tuple[int, int], Tuple[int, int]]]

        for line in f.read().splitlines():
            matched = re.match(rexp, line)
            if matched:
                points.append([
                    (int(matched[1]), int(matched[2])),
                    (int(matched[3]), int(matched[4])),
                ])

        tmp_coords = (list(zip(*[item[0] for item in points])))
        sx = max(tmp_coords[0]) - min(tmp_coords[0])
        sy = max(tmp_coords[1]) - min(tmp_coords[1])
        current_scatter = sx + sy

        stop = False
        seconds_elapsed = 0

        granularity = 10000
        while True:
            if stop:
                break
            previous_points = copy.deepcopy(points)
            # Apply velocities.
            for point in points:
                point[0] = (
                    point[0][0] + point[1][0] * granularity,
                    point[0][1] + point[1][1] * granularity,
                )

            # Calculate scatter.
            tmp_coords = (list(zip(*[item[0] for item in points])))
            min_x = min(tmp_coords[0])
            max_x = max(tmp_coords[0])
            min_y = min(tmp_coords[1])
            max_y = max(tmp_coords[1])
            sx = max_x - min_x
            sy = max_y - min_y
            scatter = sx + sy

            if scatter <= current_scatter:
                current_scatter = scatter
                seconds_elapsed += 1 * granularity
            elif granularity > 1:
                granularity /= 10
                points = copy.deepcopy(previous_points)
            else:
                print(seconds_elapsed)
                stop = True


print(timeit.timeit(run, number=1))

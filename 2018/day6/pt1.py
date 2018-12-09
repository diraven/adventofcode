"""
--- Day 6: Chronal Coordinates ---

The device on your wrist beeps several times, and once again you feel like you're falling.

"Situation critical," the device announces. "Destination indeterminate. Chronal interference detected. Please specify new target coordinates."

The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or dangerous? It recommends you check manual page 729. The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer X,Y locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).

Your goal is to find the size of the largest area that isn't infinite. For example, consider the following list of coordinates:

1, 1
1, 6
8, 3
3, 4
5, 5
8, 9

If we name these coordinates A through F, we can draw them on a grid, putting 0,0 at the top left:

..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.

This view is partial - the actual grid extends infinitely in all directions. Using the Manhattan distance, each location's closest coordinate can be determined, shown here in lowercase:

aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf

Locations shown as . are equally far from two or more coordinates, and so they don't count as being closest to any.

In this example, the areas of coordinates A, B, C, and F are infinite - while not shown here, their areas extend forever outside the visible grid. However, the areas of coordinates D and E are finite: D is closest to 9 locations, and E is closest to 17 (both including the coordinate's location itself). Therefore, in this example, the size of the largest area is 17.

What is the size of the largest area that isn't infinite?
"""
import timeit
from typing import Dict, Tuple, List

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.markers import MarkerStyle


def run() -> None:
    """
    Main function.
    """
    with open("./input.txt") as f:
        data = f.read().splitlines()

        grid = {}  # type: Dict[Tuple[int, int], Tuple[int, int]]
        points = [(int(x.split(", ")[0]), int(x.split(", ")[1])) for x in
                  data]  # type: List[Tuple[int, int]]

        colors = matplotlib.colors.get_named_colors_mapping()

        points_encode_colors = {}
        for idx, point in enumerate(points):
            points_encode_colors[point] = list(colors.values())[idx]

        # Get min and max x and y.
        max_x = 0
        max_y = 0
        for point in points:
            if point[0] > max_x:
                max_x = point[0]
            if point[1] > max_y:
                max_y = point[1]

        min_x = max_x
        min_y = max_y
        for point in points:
            if point[0] < min_x:
                min_x = point[0]
            if point[1] < min_y:
                min_y = point[1]

        print(f'max_x {max_x}, max_y {max_y}')
        print(f'min_x {min_x}, min_y {min_y}')

        # Fill grid with coords.
        for point in points:
            grid[point] = point

        # Now within minimum and maximum x and y - calculate all the points -
        # which point area are they.
        # For every x coord.
        for x in range(min_x - 1, max_x + 2):
            # For every y coord.
            for y in range(min_y - 1, max_y + 2):
                # For every point.
                distances = {}  # type: Dict[Tuple[int, int], int]
                for point in points:
                    distances[point] = abs(point[0] - x) + abs(point[1] - y)

                sorted_distances = sorted(distances.values())

                # If there are at least 2 points with the minimum distance -
                # then place belongs to no one.
                owner = None
                if sorted_distances[0] != sorted_distances[1]:
                    for point, distance in distances.items():
                        if distance == sorted_distances[0]:
                            owner = point
                            break
                grid[(x, y)] = owner

        # Now calculate how many cells does each point has as their area.
        areas = {}  # type Dict[Tuple[int, int], int]]
        for point in points:
            areas[point] = 0

        for coords, owner in grid.items():
            if owner is not None:
                areas[owner] += 1

        # Exclude points that have areas touch borders of the grid.
        for cell, owner in grid.items():
            if cell[0] == min_x - 1 or cell[0] == max_x + 1 or \
                    cell[1] == min_y - 1 or cell[1] == max_y + 1:
                try:
                    del areas[owner]
                except KeyError:
                    pass

        # for point in points:
        #     data = np.array([
        #         [cell[0], cell[1]] for cell, owner in grid.items() if
        #         owner == point
        #     ])
        #     x, y = data.T
        #     plt.scatter(x, y, marker=MarkerStyle(marker=","))

        for point in points:
            data = np.array(
                [[cell[0], cell[1]] for cell, owner in grid.items() if
                 owner == point]
            )
            x, y = data.T
            plt.scatter(x, y, c=points_encode_colors[point],
                        marker=MarkerStyle(marker="x"))

        # for cell, owner in grid.items():
        #     if owner is not None:
        #         plt.plot(
        #             cell[0],
        #             cell[1],
        #             c=points_encode_colors[owner],
        #             marker=",",
        #         )

        for point in points:
            plt.plot(
                point[0],
                point[1],
                c='g',
                marker="o",
            )

        for point in areas:
            plt.plot(
                point[0],
                point[1],
                c='r',
                marker="x",
            )

        # data = np.array([[point[0], point[1]] for point in points])
        # x, y = data.T
        # plt.scatter(x, y, marker=))

        # data = np.array([[point[0], point[1]] for point in areas])
        # x, y = data.T
        # plt.scatter(x, y, marker=MarkerStyle(marker="x"))

        # plt.gca().invert_yaxis()
        plt.ylim(min_y - 2, max_y + 2)
        plt.xlim(min_x - 2, max_x + 2)

        plt.savefig('result.png', dpi=1000)

        print(areas)

        print(max(areas.values()))


print(timeit.timeit(run, number=1))
# 3930 too high
# 3970 too high

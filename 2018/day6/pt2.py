"""
--- Part Two ---

On the other hand, if the coordinates are safe, maybe the best you can do is try to find a region near as many coordinates as possible.

For example, suppose you want the sum of the Manhattan distance to all of the coordinates to be less than 32. For each location, add up the distances to all of the given coordinates; if the total of those distances is less than 32, that location is within the desired region. Using the same coordinates as above, the resulting region looks like this:

..........
.A........
..........
...###..C.
..#D###...
..###E#...
.B.###....
..........
..........
........F.

In particular, consider the highlighted location 4,3 located at the top middle of the region. Its calculation is as follows, where abs() is the absolute value function:

    Distance to coordinate A: abs(4-1) + abs(3-1) =  5
    Distance to coordinate B: abs(4-1) + abs(3-6) =  6
    Distance to coordinate C: abs(4-8) + abs(3-3) =  4
    Distance to coordinate D: abs(4-3) + abs(3-4) =  2
    Distance to coordinate E: abs(4-5) + abs(3-5) =  3
    Distance to coordinate F: abs(4-8) + abs(3-9) = 10
    Total distance: 5 + 6 + 4 + 2 + 3 + 10 = 30

Because the total distance to all coordinates (30) is less than 32, the location is within the region.

This region, which also includes coordinates D and E, has a total size of 16.

Your actual region will need to be much larger than this example, though, instead including all locations with a total distance of less than 10000.

What is the size of the region containing all locations which have a total distance to all given coordinates of less than 10000?
"""
import timeit
from typing import Tuple, List


def run() -> None:
    """
    Main function.
    """
    with open("./input.txt") as f:
        data = f.read().splitlines()

        points = [(int(x.split(", ")[0]), int(x.split(", ")[1])) for x in
                  data]  # type: List[Tuple[int, int]]

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

        target_distance = 10000
        # Now calculate left, right, top and bottom boundaries.

        # bound_left = math.floor(max_x - (target_distance / len(points)))
        # bound_right = math.ceil(min_x + (target_distance / len(points)))
        # bound_bottom = math.floor(max_y - (target_distance / len(points)))
        # bound_top = math.ceil(min_y + (target_distance / len(points)))

        # Now for each grid cell within the calculated boundaries - check
        # if it's inside the region.
        counter = 0
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                distance = 0
                for point in points:
                    distance += abs(point[0] - x) + abs(point[1] - y)
                if distance < target_distance:
                    counter += 1

        print(counter)


# 9744 too low
# 38157 too low

print(timeit.timeit(run, number=1))

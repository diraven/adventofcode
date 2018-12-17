"""
--- Day 17: Reservoir Research ---

You arrive in the year 18. If it weren't for the coat you got in 1018, you would be very cold: the North Pole base hasn't even been constructed.

Rather, it hasn't been constructed yet. The Elves are making a little progress, but there's not a lot of liquid water in this climate, so they're getting very dehydrated. Maybe there's more underground?

You scan a two-dimensional vertical slice of the ground nearby and discover that it is mostly sand with veins of clay. The scan only provides data with a granularity of square meters, but it should be good enough to determine how much water is trapped there. In the scan, x represents the distance to the right, and y represents the distance down. There is also a spring of water near the surface at x=500, y=0. The scan identifies which square meters are clay (your puzzle input).

For example, suppose your scan shows the following veins of clay:

x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504

Rendering clay as #, sand as ., and the water spring as +, and with x increasing to the right and y increasing downward, this becomes:

   44444455555555
   99999900000000
   45678901234567
 0 ......+.......
 1 ............#.
 2 .#..#.......#.
 3 .#..#..#......
 4 .#..#..#......
 5 .#.....#......
 6 .#.....#......
 7 .#######......
 8 ..............
 9 ..............
10 ....#.....#...
11 ....#.....#...
12 ....#.....#...
13 ....#######...

The spring of water will produce water forever. Water can move through sand, but is blocked by clay. Water always moves down when possible, and spreads to the left and right otherwise, filling space that has clay on both sides and falling out otherwise.

For example, if five squares of water are created, they will flow downward until they reach the clay and settle there. Water that has come to rest is shown here as ~, while sand through which water has passed (but which is now dry again) is shown as |:

......+.......
......|.....#.
.#..#.|.....#.
.#..#.|#......
.#..#.|#......
.#....|#......
.#~~~~~#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...

Two squares of water can't occupy the same location. If another five squares of water are created, they will settle on the first five, filling the clay reservoir a little more:

......+.......
......|.....#.
.#..#.|.....#.
.#..#.|#......
.#..#.|#......
.#~~~~~#......
.#~~~~~#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...

Water pressure does not apply in this scenario. If another four squares of water are created, they will stay on the right side of the barrier, and no water will reach the left side:

......+.......
......|.....#.
.#..#.|.....#.
.#..#~~#......
.#..#~~#......
.#~~~~~#......
.#~~~~~#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...

At this point, the top reservoir overflows. While water can reach the tiles above the surface of the water, it cannot settle there, and so the next five squares of water settle like this:

......+.......
......|.....#.
.#..#||||...#.
.#..#~~#|.....
.#..#~~#|.....
.#~~~~~#|.....
.#~~~~~#|.....
.#######|.....
........|.....
........|.....
....#...|.#...
....#...|.#...
....#~~~~~#...
....#######...

Note especially the leftmost |: the new squares of water can reach this tile, but cannot stop there. Instead, eventually, they all fall to the right and settle in the reservoir below.

After 10 more squares of water, the bottom reservoir is also full:

......+.......
......|.....#.
.#..#||||...#.
.#..#~~#|.....
.#..#~~#|.....
.#~~~~~#|.....
.#~~~~~#|.....
.#######|.....
........|.....
........|.....
....#~~~~~#...
....#~~~~~#...
....#~~~~~#...
....#######...

Finally, while there is nowhere left for the water to settle, it can reach a few more tiles before overflowing beyond the bottom of the scanned data:

......+.......    (line not counted: above minimum y value)
......|.....#.
.#..#||||...#.
.#..#~~#|.....
.#..#~~#|.....
.#~~~~~#|.....
.#~~~~~#|.....
.#######|.....
........|.....
...|||||||||..
...|#~~~~~#|..
...|#~~~~~#|..
...|#~~~~~#|..
...|#######|..
...|.......|..    (line not counted: below maximum y value)
...|.......|..    (line not counted: below maximum y value)
...|.......|..    (line not counted: below maximum y value)

How many tiles can be reached by the water? To prevent counting forever, ignore tiles with a y coordinate smaller than the smallest y coordinate in your scan data or larger than the largest one. Any x coordinate is valid. In this example, the lowest y coordinate given is 1, and the highest is 13, causing the water spring (in row 0) and the water falling off the bottom of the render (in rows 14 through infinity) to be ignored.

So, in the example above, counting both water at rest (~) and other sand tiles the water can hypothetically reach (|), the total number of tiles the water can reach is 57.

How many tiles can the water reach within the range of y values in your scan?
"""
import timeit

SAND = '.'
CLAY = '#'
WATER_SOURCE = '+'
WATER_FLOWING = '|'
WATER_STILL = '~'


class Grid:
    def __init__(self, data: str) -> None:
        self.grid = {}
        self.sources = []
        for row in data.splitlines():
            first, second = row.split(', ')
            axis1, value1 = first.split('=')
            axis2, value2 = second.split('=')
            value2_min, value2_max = value2.split('..')
            if axis1 == 'x':
                x = int(value1)
                for y in range(int(value2_min), int(value2_max) + 1):
                    if y not in self.grid:
                        self.grid[y] = {}
                    self.grid[y][x] = CLAY

            if axis1 == 'y':
                y = int(value1)
                if y not in self.grid:
                    self.grid[y] = {}
                for x in range(int(value2_min), int(value2_max) + 1):
                    self.grid[y][x] = CLAY

        self.min_input_y = min(self.grid.keys())

        # Set water source.
        if 0 not in self.grid:
            self.grid[0] = {}
        self.add_source(0, 500)

        keys = self.grid.keys()
        self.min_y = min(keys)
        self.max_y = max(keys)

        values = set()
        for row in self.grid.values():
            for key in row.keys():
                values.add(key)
        self.min_x = min(values) - 1
        self.max_x = max(values) + 1

        # Fill empty grid with sand.
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                if y not in self.grid:
                    self.grid[y] = {}
                if x not in self.grid[y]:
                    self.grid[y][x] = SAND

    def add_source(self, y: int, x: int):
        self.grid[y][x] = WATER_SOURCE
        self.sources.append((y, x))

    def remove_source(self, y: int, x: int):
        self.sources.remove((y, x))

    def tick(self) -> bool:
        if len(self.sources) == 0:
            return False

        # From each source try to go bottom.
        for y, x in self.sources.copy():
            # Check if current cell is still source:
            if self.grid[y][x] != WATER_SOURCE:
                self.remove_source(y, x)
                continue

            # Current cell is not source any more.
            self.remove_source(y, x)
            self.grid[y][x] = WATER_FLOWING

            # If cell below source is still within bounds:
            if y + 1 in self.grid:
                # If water below is flowing - we do nothing.
                if self.grid[y + 1][x] == WATER_FLOWING:
                    continue

                # If sand is below - place the source there.
                if self.grid[y + 1][x] == SAND:
                    self.add_source(y + 1, x)
                    continue

                # Try to place water all the way left until it can go below.
                went_below = False
                left_x = x
                right_x = x

                curr_x = x - 1
                while self.grid[y][curr_x] in [SAND, WATER_FLOWING,
                                               WATER_SOURCE]:
                    self.grid[y][curr_x] = WATER_FLOWING
                    left_x = curr_x
                    # Check if we can put water below.
                    if y + 1 in self.grid:
                        if self.grid[y + 1][curr_x] in [SAND, WATER_FLOWING]:
                            self.add_source(y + 1, curr_x)
                            went_below = True
                            break
                    curr_x -= 1

                # Try to place water all the way right until it can go below.
                curr_x = x + 1
                while self.grid[y][curr_x] in [SAND, WATER_FLOWING,
                                               WATER_SOURCE]:
                    self.grid[y][curr_x] = WATER_FLOWING
                    right_x = curr_x
                    # Check if we can put water below.
                    if y + 1 in self.grid:
                        if self.grid[y + 1][curr_x] in [SAND, WATER_FLOWING]:
                            self.add_source(y + 1, curr_x)
                            went_below = True
                            break
                    curr_x += 1

                if went_below:
                    continue

                # If water did not went below - all the water we have just
                # placed including our original water piece is now still water.
                for flowing_x in range(left_x, right_x + 1):
                    self.grid[y][flowing_x] = WATER_STILL
                    if self.grid[y - 1][flowing_x] == WATER_FLOWING:
                        self.add_source(y - 1, flowing_x)

        return True

    def __str__(self) -> str:
        result = ""
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                result += self.grid[y][x]
            result += '\n'
        return result

    def __eq__(self, other: 'Grid') -> bool:
        return str(self) == str(other)


def run() -> None:
    """
    Main function.
    """
    with open("./input.txt") as f:
        grid = Grid(f.read())

        has_sources = True
        counter = 0
        while has_sources:
            counter += 1
            has_sources = grid.tick()
            # print(counter)

        str_grid = str(grid)
        water_count = str_grid.count('~') + str_grid.count(
            '|') - grid.min_input_y
        print(water_count)


print(f"{timeit.timeit(run, number=1)} sec")

"""
--- Part Two ---

After a very long time, the water spring will run dry. How much water will be retained?

In the example above, water that won't eventually drain out is shown as ~, a total of 29 tiles.

How many water tiles are left after the water spring stops producing water and all remaining water not at rest has drained?
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
        water_count = str_grid.count('~')
        print(water_count)


print(f"{timeit.timeit(run, number=1)} sec")

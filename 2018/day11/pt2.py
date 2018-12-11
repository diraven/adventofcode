"""
--- Part Two ---

You discover a dial on the side of the device; it seems to let you select a square of any size, not just 3x3. Sizes from 1x1 to 300x300 are supported.

Realizing this, you now must find the square of any size with the largest total power. Identify this square by including its size as a third parameter after the top-left coordinate: a 9x9 square with a top-left corner of 3,5 is identified as 3,5,9.

For example:

    For grid serial number 18, the largest total square (with a total power of 113) is 16x16 and has a top-left corner of 90,269, so its identifier is 90,269,16.
    For grid serial number 42, the largest total square (with a total power of 119) is 12x12 and has a top-left corner of 232,251, so its identifier is 232,251,12.

What is the X,Y,size identifier of the square with the largest total power?
"""
import math
import timeit

import numpy as np


def run() -> None:
    """
    Main function.
    """
    # with open("./input.example.txt") as f:
    with open("./input.txt") as f:
        serial_number = int(f.read())

        grid_size = 300
        power_cells = np.zeros((grid_size, grid_size), dtype=np.int)
        for x in range(grid_size):
            for y in range(grid_size):
                rack_id = x + 10 + 1
                power = rack_id * (y + 1)
                power += serial_number
                power *= rack_id
                try:
                    power = int(str(power)[-3])
                    power -= 5
                except IndexError:
                    power = 0

                power_cells[x, y] = power

        print("done")

        # current_cell = (90, 269, 16)
        # current_total_power = 113
        # min_size = 4
        current_cell = (0, 0, 0)
        current_total_power = 0
        min_size = 1

        max_possible_power = 0
        for x in range(grid_size):
            for y in range(grid_size):
                if power_cells[x][y] > 0:
                    max_possible_power += power_cells[x][y]
        max_size = math.ceil(math.sqrt(max_possible_power / 5))
        print(max_size)

        for x in range(grid_size):
            for y in range(grid_size):
                for size in range(min_size,
                                  min(grid_size - max(x, y) + 1, max_size)):
                    total_power = np.sum(power_cells[x:x + size, y:y + size])
                    if total_power > current_total_power:
                        current_cell = (x + 1, y + 1, size)
                        current_total_power = total_power
                        min_size = math.floor(
                            math.sqrt(current_total_power / 5))

        print(current_cell)


# not 28,75,13
# not 90,269,16
print(timeit.timeit(run, number=1))

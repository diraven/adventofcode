"""
https://adventofcode.com/2018/day/3
"""
import timeit


def run() -> None:
    """
    Main function.
    """
    heat_map = [[0 for x in range(1000)] for x in range(1000)]

    with open("./input.txt") as f:
        # 1 @ 335,861: 14x10
        for line in f.read().splitlines():
            origin_size = line.split('@')[1].strip().split(': ')
            origin = origin_size[0].split(',')
            size = origin_size[1].split('x')
            for x in range(int(origin[0]), int(origin[0])+int(size[0])):
                for y in range(int(origin[1]), int(origin[1])+int(size[1])):
                    heat_map[x][y] += 1

        counter = 0
        for row in heat_map:
            for heat in row:
                if heat > 1:
                    counter += 1

        print(counter)


print(timeit.timeit(run, number=1))

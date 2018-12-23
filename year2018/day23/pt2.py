"""
--- Part Two ---

Now, you just need to figure out where to position yourself so that you're actually teleported when the nanobots activate.

To increase the probability of success, you need to find the coordinate which puts you in range of the largest number of nanobots. If there are multiple, choose one closest to your position (0,0,0, measured by manhattan distance).

For example, given the following nanobot formation:

pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5

Many coordinates are in range of some of the nanobots in this formation. However, only the coordinate 12,12,12 is in range of the most nanobots: it is in range of the first five, but is not in range of the nanobot at 10,10,10. (All other coordinates are in range of fewer than five nanobots.) This coordinate's distance from 0,0,0 is 36.

Find the coordinates that are in range of the largest number of nanobots. What is the shortest manhattan distance between any of those points and 0,0,0?
"""
import itertools
from typing import List

import numpy as np


class Location:
    def __init__(self, bots, x: int, y: int, z: int) -> None:
        self.x = x  # type: int
        self.y = y  # type: int
        self.z = z  # type: int
        self.bots_in_range = 0
        for bot in bots:
            if self.distance_to(bot) <= bot.strength:
                self.bots_in_range += 1

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'

    def distance_to(self, other: 'Location') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(
            self.z - other.z)


class Bot(Location):
    def __init__(self, bots, x: int, y: int, z: int, strength: int) -> None:
        super().__init__(bots, x, y, z)
        self.strength = strength
        self.bots_in_range_count = 0

    def __str__(self):
        return f'{super().__str__()}: {self.strength}, {self.bots_in_range_count}'


def main():
    bots = []  # type: List[Bot]
    with open("input.txt") as f:
        data = f.read().splitlines()

        for line in data:
            splitted = line.split(', ')
            position = splitted[0].replace('pos=<', '').rstrip('>').split(',')
            strength = splitted[1].replace('r=', '')
            bots.append(
                Bot(bots, *([int(coord) for coord in position] + [int(strength)]))
            )

        heated_coords = []
        for i, axis in enumerate('xyz'):
            print(axis)
            heated_coords.append([])
            vals = [getattr(b, axis) for b in bots]
            min_val = min(vals)
            max_val = max(vals)
            width = max_val - min_val
            heat = np.full(width, dtype=np.int, fill_value=0)
            for bot in bots:
                print(bot)
                for val in range(
                        max(getattr(bot, axis) - bot.strength, min_val),
                        min(getattr(bot, axis) + bot.strength, max_val)
                ):
                    heat[val - min_val] += 1
            max_heat = np.max(heat)
            for v, heat in enumerate(heat):
                if heat == max_heat:
                    heated_coords[i].append(v + min_val)
            print('done')

        best_location = None
        origin = Location(bots, 0, 0, 0)
        for coords_set in list(itertools.product(*heated_coords)):
            location = Location(bots, coords_set[0], coords_set[1],
                                coords_set[2])
            if not best_location:
                best_location = location
            else:
                if location.bots_in_range > best_location.bots_in_range:
                    best_location = location
                elif location.bots_in_range == best_location.bots_in_range \
                        and \
                        location.distance_to(origin) < \
                        best_location.distance_to(origin):
                    best_location = location

        print(best_location.distance_to(origin))


main()

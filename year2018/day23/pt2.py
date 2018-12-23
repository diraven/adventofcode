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
from collections import namedtuple
from typing import List

Bot = namedtuple('Bot', ('x', 'y', 'z', 'strength'))
Loc = namedtuple('Location', ('x', 'y', 'z', 'bots_in_range_count'))


class Location(Loc):
    def distance_to(self, other: 'Location') -> int:
        if not hasattr(self, 'distances'):
            self.distances = {}
        if other not in self.distances:
            self.distances[other] = abs(self.x - other.x) + \
                                    abs(self.y - other.y) + \
                                    abs(self.z - other.z)

        return self.distances[other]


def find_best_locations(
        bots: List[Bot],
        step: int,
        min_x: int,
        max_x: int,
        min_y: int,
        max_y: int,
        min_z: int,
        max_z: int,
) -> List[Location]:
    locations = []
    for x in range(min_x, max_x + 1, step):
        for y in range(min_y, max_y + 1, step):
            for z in range(min_z, max_z + 1, step):
                bots_in_range_count = 0
                for bot in bots:
                    distance = abs(bot.x - x) + abs(
                        bot.y - y) + abs(bot.z - z)
                    if distance <= bot.strength:
                        bots_in_range_count += 1
                        locations.append(
                            Location(x, y, z, bots_in_range_count))

    # Pick best locations.
    max_bots_in_range = max(l.bots_in_range_count for l in locations)
    locations = [l for l in locations if
                 l.bots_in_range_count == max_bots_in_range]

    my_location = Location(0, 0, 0, 0)
    min_distance = min(l.distance_to(my_location) for l in locations)
    resulting_locations = [l for l in locations if
                           l.distance_to(my_location) == min_distance]

    if locations:
        print(len(locations), step)

    if step > 2:
        locations = set()
        for location in resulting_locations:
            for l in find_best_locations(
                    bots,
                    int(step / 2),
                    location.x - step,
                    location.x + step,
                    location.y - step,
                    location.y + step,
                    location.z - step,
                    location.z + step,
            ):
                locations.add(l)

    return resulting_locations


def main() -> None:
    bots = []  # type: List[Bot]

    with open("input.txt") as f:
        data = f.read().splitlines()

        for line in data:
            splitted = line.split(', ')
            position = splitted[0].replace('pos=<', '').rstrip('>').split(',')
            strength = splitted[1].replace('r=', '')
            bots.append(
                Bot(*([int(coord) for coord in position] + [int(strength)]))
            )

        min_x = min(bot.x for bot in bots)
        max_x = max(bot.x for bot in bots)

        min_y = min(bot.y for bot in bots)
        max_y = max(bot.y for bot in bots)

        min_z = min(bot.z for bot in bots)
        max_z = max(bot.z for bot in bots)

        step = 10 ** 7
        locations = find_best_locations(
            bots, step, min_x, max_x, min_y, max_y, min_z, max_z
        )

        [print(f'{l} {l.distance_to(Location(0, 0, 0, 0))}') for l in
         locations]

    # print(location.distance_to(Location(0, 0, 0, 0)))
    # 86012062 too low
    # 86012062
    # 86012062
    # 86012063 too low


main()

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
Location = namedtuple('Location', ('x', 'y', 'z'))

step_divisor = 5

total_low_level = 0


def filter_locations(
        bots: List[Bot],
        locations: List[Location],
) -> List[Location]:
    calculated_locations = {}
    for l in locations:
        in_range = 0
        for b in bots:
            if abs(b.x - l.x) + abs(b.y - l.y) + abs(
                    b.z - l.z) <= b.strength:
                in_range += 1
        calculated_locations[l] = in_range

    # Find maximum amount of bots in range.
    max_in_range = max(calculated_locations.values())

    distanced_locations = {}
    # Build a list of locations with the highest amount of bots in range.
    for l, in_range in calculated_locations.items():
        if in_range == max_in_range:
            distanced_locations[l] = abs(l.x) + abs(l.y) + abs(l.z)

    # Find minimum distance to the origin.
    min_distance = min(distanced_locations.values())

    print(min_distance)

    # Pick locations that are closest to the origin.
    filtered_locations = set()
    for l, distance in distanced_locations.items():
        if distance == min_distance:
            filtered_locations.add(l)

    print(len(filtered_locations))

    return [filtered_locations.pop()] if filtered_locations else []


def search(bots, min_x, max_x, min_y, max_y, min_z, max_z, step,
           depth: int = 0) -> List[
    Location
]:
    global total_low_level

    locations = []
    for x in range(max_x + step, min_x, -step):
        for y in range(max_y + step, min_y, -step):
            for z in range(max_z + step, min_z, -step):
                locations.append(Location(x, y, z))

    filtered_locations = filter_locations(bots, locations)

    if step > 1:
        print(
            f'''
            found {len(filtered_locations)} locations, 
            step {step} at depth {depth}
            '''
        )

    if step == 1:
        return filtered_locations
    else:
        if step < step_divisor:
            new_step = 1
        else:
            new_step = int(step / step_divisor)

        resulting_locations = []
        for l in filtered_locations:
            resulting_locations += search(
                bots=bots,
                min_x=l.x - step,
                max_x=l.x + step,
                min_y=l.y - step,
                max_y=l.y + step,
                min_z=l.z - step,
                max_z=l.z + step,
                step=new_step,
                depth=depth + 1,
            )
        return filter_locations(bots, resulting_locations)


def main():
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

        min_x = min(b.x for b in bots)
        min_y = min(b.y for b in bots)
        min_z = min(b.z for b in bots)
        max_x = max(b.x for b in bots)
        max_y = max(b.y for b in bots)
        max_z = max(b.z for b in bots)

        width = max_x - min_x
        height = max_y - min_y
        depth = max_z - min_z

        step = int(min(width, height, depth) / 30)

        locations = search(
            bots,
            min_x,
            max_x,
            min_y,
            max_y,
            min_z,
            max_z,
            step
        )

        print(sum(filter_locations(bots, locations)[0]))


# 73223365 too low
# 86012062 too low
main()

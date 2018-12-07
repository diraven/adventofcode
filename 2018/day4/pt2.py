"""
https://adventofcode.com/2018/day/4

--- Part Two ---

Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?

In the example above, Guard #99 spent minute 45 asleep more than any other guard or minute - three times in total. (In all other cases, any guard spent any minute asleep at most twice.)

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 99 * 45 = 4455.)
"""

import timeit
from typing import Dict, List


def run() -> None:
    """
    Main function.
    """
    with open("./input.txt") as f:
        # Load and sort the data.
        data = sorted(f.read().splitlines())

        # Init variables.
        guard_date_patterns = {}  # type: Dict[str, Dict[str, List[int]]]
        current_guard_id = 0
        fell_asleep_at_minute = 0

        # For each item.
        for item in data:
            # Guard id line.
            if "Guard" in item:
                current_guard_id = item.split()[3].lstrip('#')

            # Falls asleep line.
            if "falls asleep" in item:
                fell_asleep_at_minute = int(
                    item.split()[1].rstrip(']').split(':')[1])

            # Wakes up line.
            if "wakes up" in item:
                woke_up_at_minute = int(
                    item.split()[1].rstrip(']').split(':')[1])

                # Save the pattern for the day.
                pattern = [0] * 60
                for i in range(fell_asleep_at_minute, woke_up_at_minute):
                    pattern[i] = 1
                date = item.split()[0].lstrip("[")

                if current_guard_id not in guard_date_patterns:
                    guard_date_patterns[current_guard_id] = {}

                # Make sure to adjust pattern instead of replacing it if
                # the guard falls asleep and awakes multiple times during
                # the same day.
                if date not in guard_date_patterns[current_guard_id]:
                    guard_date_patterns[current_guard_id][date] = pattern
                else:
                    guard_date_patterns[current_guard_id][date] = [
                        sum(x) for x in zip(
                            guard_date_patterns[current_guard_id][date],
                            pattern
                        )
                    ]

        # Now calculate sleeping patterns per guard as opposed to per guard per
        # day.
        guard_patterns = {}  # type: Dict[str, List[int]]
        for gid, guard in guard_date_patterns.items():
            guard_patterns[gid] = [sum(x) for x in zip(*guard.values())]

        # Now get the most sleepy minute of the most sleepy guard:
        minute_idx = 0
        sleepy_guard_id = 0
        max_times_slept = 0
        for gid, guard_pattern in guard_patterns.items():
            for i, times_slept in enumerate(guard_pattern):
                if times_slept > max_times_slept:
                    max_times_slept = times_slept
                    sleepy_guard_id = gid
                    minute_idx = i

        print(minute_idx * int(sleepy_guard_id))


print(timeit.timeit(run, number=1))

"""
https://adventofcode.com/2018/day/1
"""


def run():
    """
    Looks for the repeated frequency.
    :return:
    """
    with open("./input.txt") as f:
        deltas = [int(n) for n in f.read().splitlines()]

        current_freq = 0
        reached_freqs = []

        while True:
            for delta in deltas:
                print(current_freq)

                if current_freq in reached_freqs:
                    print(f'found: {current_freq}')
                    return

                reached_freqs.append(current_freq)
                current_freq += delta


run()

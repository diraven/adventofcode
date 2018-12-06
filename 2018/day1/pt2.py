"""
https://adventofcode.com/2018/day/1

--- Part Two ---

You notice that the device repeats the same frequency change list over and over. To calibrate the device, you need to find the first frequency it reaches twice.

For example, using the same list of changes above, the device would loop as follows:

    Current frequency  0, change of +1; resulting frequency  1.
    Current frequency  1, change of -2; resulting frequency -1.
    Current frequency -1, change of +3; resulting frequency  2.
    Current frequency  2, change of +1; resulting frequency  3.
    (At this point, the device continues from the start of the list.)
    Current frequency  3, change of +1; resulting frequency  4.
    Current frequency  4, change of -2; resulting frequency  2, which has already been seen.

In this example, the first frequency reached twice is 2. Note that your device might need to repeat its list of frequency changes many times before a duplicate frequency is found, and that duplicates might be found while in the middle of processing the list.

Here are other examples:

    +1, -1 first reaches 0 twice.
    +3, +3, +4, -2, -4 first reaches 10 twice.
    -6, +3, +8, +5, -6 first reaches 5 twice.
    +7, +7, -2, -7, -4 first reaches 14 twice.

What is the first frequency your device reaches twice?
"""

def run():
    """
    Looks for the repeated frequency.
    :return:
    """
    with open("./input.txt") as f:
        deltas = [int(n) for n in f.read().splitlines()]

        current_freq = 0
        reached_freqs = set()

        while True:
            for delta in deltas:
                print(current_freq)

                if current_freq in reached_freqs:
                    print(f'found: {current_freq}')
                    return

                reached_freqs.add(current_freq)
                current_freq += delta


run()

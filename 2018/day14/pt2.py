"""
--- Part Two ---

As it turns out, you got the Elves' plan backwards. They actually want to know how many recipes appear on the scoreboard to the left of the first recipes whose scores are the digits from your puzzle input.

    51589 first appears after 9 recipes.
    01245 first appears after 5 recipes.
    92510 first appears after 18 recipes.
    59414 first appears after 2018 recipes.

How many recipes appear on the scoreboard to the left of the score sequence in your puzzle input?
"""

from collections import deque
import timeit


def run() -> None:
    """
    Main function.
    """
    with open("./input.txt") as f:
        # Load data.
        data = f.read().strip()
        # data = "59414"
        sequence_length = len(data)

        recipes = deque([3, 7])
        offset1 = 0
        offset2 = 1

        recipes_count = 2

        output_counter = 0
        while True:
            output_counter += 1
            sum_ = recipes[offset1] + recipes[offset2]
            for digit in str(sum_):
                recipes.append(int(digit))
                recipes_count += 1

            offset1 = (offset1 + recipes[offset1] + 1) % recipes_count
            offset2 = (offset2 + recipes[offset2] + 1) % recipes_count

            sample = ""
            for i in range(sequence_length + 1):
                recipes.rotate(1)
                sample += str(recipes[0])

            sample = list(reversed(sample))
            if sample[:-1] == data:
                print(recipes_count - sequence_length + 1)
                return
            if sample[1:] == data:
                print(recipes_count - sequence_length)
                return

            recipes.rotate(-sequence_length - 1)

            if output_counter == 100000:
                print(f"{recipes_count}")
                output_counter = 0


print(f"{timeit.timeit(run, number=1)} sec")

"""
--- Part Two ---

As it turns out, you got the Elves' plan backwards. They actually want to know how many recipes appear on the scoreboard to the left of the first recipes whose scores are the digits from your puzzle input.

    51589 first appears after 9 recipes.
    01245 first appears after 5 recipes.
    92510 first appears after 18 recipes.
    59414 first appears after 2018 recipes.

How many recipes appear on the scoreboard to the left of the score sequence in your puzzle input?
"""

import timeit

from blist import blist


def run() -> None:
    """
    Main function.
    """
    with open("./input.txt") as f:
        # Load data.
        # data = "51589" #first appears after 9 recipes.
        # data = "01245" #first appears after 5 recipes.
        # data = "92510" #first appears after 18 recipes.
        # data = "59414" #first appears after 2018 recipes.

        # data = "59414"
        # data = "01245"

        # data = "260321"  # 20M?

        data = f.read().strip()
        # data = "540391" # ???

        data = [int(digit) for digit in data]
        sequence_length = len(data)

        recipes = blist([3, 7])
        offset1 = 0
        offset2 = 1

        recipes_count = 2

        while True:
            sum_ = recipes[offset1] + recipes[offset2]
            for digit in str(sum_):
                recipes.append(int(digit))
                recipes_count += 1

            offset1 = (offset1 + recipes[offset1] + 1) % recipes_count
            offset2 = (offset2 + recipes[offset2] + 1) % recipes_count

            if recipes[-sequence_length:] == data:
                print(recipes_count - sequence_length)
                return
            if recipes[-sequence_length - 1:-1] == data:
                print(recipes_count - sequence_length - 1)
                return


print(f"{timeit.timeit(run, number=1)} sec")

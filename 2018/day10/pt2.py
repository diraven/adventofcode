"""
Amused by the speed of your answer, the Elves are curious:

What would the new winning Elf's score be if the number of the last marble were 100 times larger?
"""
import timeit
from typing import List

from blist import blist

Circle = List[int]


def run() -> None:
    """
    Main function.
    """
    with open("./input.txt") as f:
        data = f.read().splitlines()[0].split()
        players_count = int(data[0])
        last_marble_worth = int(data[6]) * 100

        current_idx = 0
        current_player = 0
        circle = blist([0])
        current_player += 1

        scores = {}
        for player in range(players_count):
            scores[player] = 0

        circle_len = 1

        for i in range(1, last_marble_worth):
            if i % 23 == 0:
                scores[current_player] += i
                current_idx = (current_idx - 7) % circle_len
                scores[current_player] += circle.pop(current_idx)
                circle_len -= 1
                if current_idx > circle_len - 1:
                    current_idx = 0
            else:
                if circle_len > 1:
                    current_idx = (current_idx + 2) % circle_len
                else:
                    current_idx = 1
                circle.insert(current_idx, i)
                circle_len += 1

            if current_player == players_count - 1:
                current_player = 0
            else:
                current_player += 1

        print(max(scores.values()))


print(timeit.timeit(run, number=1))

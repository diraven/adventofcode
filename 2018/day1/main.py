"""
https://adventofcode.com/2018/day/1
"""

with open("./input.txt") as f:
    print(sum([int(n) for n in f.read().splitlines()]))

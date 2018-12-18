"""
--- Part Two ---

This important natural resource will need to last for at least thousands of years. Are the Elves collecting this lumber sustainably?

What will the total resource value of the lumber collection area be after 1000000000 minutes?
"""
from typing import List


# This one was done manually by finding the repeating period, which was 28
# in my case and then figuring out which count of that repeating period
# will situation end up in 1000000000 cycles.

def get_neighbours(lines: List[str], line_n: int, char_n: int) -> str:
    neighbours = ""
    if line_n > 0:
        if char_n > 0:
            neighbours += lines[line_n - 1][char_n - 1]
        neighbours += lines[line_n - 1][char_n]
        if char_n < len(lines[0]) - 1:
            neighbours += lines[line_n - 1][char_n + 1]

    if line_n < len(lines) - 1:
        if char_n > 0:
            neighbours += lines[line_n + 1][char_n - 1]
        neighbours += lines[line_n + 1][char_n]
        if char_n < len(lines[0]) - 1:
            neighbours += lines[line_n + 1][char_n + 1]

    if char_n > 0:
        neighbours += lines[line_n][char_n - 1]

    if char_n < len(lines[0]) - 1:
        neighbours += lines[line_n][char_n + 1]

    return neighbours


def mutate_char(state, line_n, char_n) -> str:
    if state[line_n][char_n] == '.':
        if get_neighbours(
                state, line_n, char_n
        ).count('|') >= 3:
            return '|'

    if state[line_n][char_n] == '|':
        if get_neighbours(
                state, line_n, char_n
        ).count('#') >= 3:
            return '#'

    if state[line_n][char_n] == '#':
        neighbours = get_neighbours(state, line_n, char_n)
        if neighbours.count('#') == 0 or neighbours.count('|') == 0:
            return '.'

    return state[line_n][char_n]


def run() -> None:
    """
    Main function.
    """
    with open("./input.txt") as f:
        state = f.read().split()

        # print('\n'.join(state))

        period = 28

        counts = []
        pattern = []
        pattern_start = 0
        for i in range(1000):
            new_state = state.copy()
            for line_n, line in enumerate(state):
                for char_n, char in enumerate(state):
                    new_state[line_n] = new_state[line_n][:char_n] \
                                        + mutate_char(state, line_n, char_n) \
                                        + new_state[line_n][char_n + 1:]

            state = new_state
            final_state = ''.join(state)
            counts.append(final_state.count("|") * final_state.count("#"))

            if len(counts) > period * 2:
                if counts[-period:] == counts[-period * 2:-period]:
                    pattern = counts[-period * 2:-period]
                    pattern_start = i - 2 * period
                    print("\n".join([str(x) for x in pattern]))
                    print("\n")
                    print("\n".join([
                        str(k) + " " + str(x) for k, x in enumerate(counts[
                                                                    pattern_start:pattern_start + 2
                                                                    ])
                    ]))
                    break

        print("\n")
        print(pattern[(1000000000 - pattern_start - 2) % period])
        print(min(pattern))


run()

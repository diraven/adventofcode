"""
--- Part Two ---

You realize that 20 generations aren't enough. After all, these plants will need to last another 1500 years to even reach your timeline, not to mention your future.

After fifty billion (50000000000) generations, what is the sum of the numbers of all pots which contain a plant?
"""
import timeit
from typing import Tuple, Dict


def find_all(string, sub):
    indicies = []
    offset = 0

    i = string.find(sub, offset)
    while i >= 0:
        indicies.append(i)
        i = string.find(sub, i + 1)
    return indicies


def normalize(state: str, offset: int, padding: int) -> Tuple[str, int]:
    offset -= state.find('#')
    state = state.strip('.')
    offset += padding
    state = '.' * padding + state + '.' * padding

    return state, offset


def build_new_generation(templates: Dict[str, str], state: str) -> str:
    new_state = '.' * len(state)
    for i in range(len(state) - 3):  # 5 is sample width
        for k, v in templates.items():
            template_idx = find_all(state, k)
            for idx in template_idx:
                new_state = new_state[:idx + 2] + v + \
                            new_state[idx + 2 + 1:]
    return new_state


def run() -> None:
    """
    Main function.
    """
    padding = 5
    generations = 50000000000

    templates = {}
    with open("./input.txt") as f:
        # Load data.
        data = f.read().splitlines()

        # Parse templates.
        for line in data[1:]:
            if line:
                splitted = line.split(' => ')
                templates[splitted[0]] = splitted[1]

        # Build initial state.
        state = data[0].replace('initial state: ', '')
        offset = 0

        generation_idx = 0
        for generation_idx in range(generations):
            state, offset = normalize(state, offset, padding)
            # print(f"# {generation_idx:03}: {state} ({offset})")
            new_state = build_new_generation(templates, state)

            if state.strip('.') == new_state.strip('.'):
                break

            state = new_state

        # Now generate required result:
        result = 0
        for i, v in enumerate(state):
            if v == "#":
                result += i - offset

        result += (generations - generation_idx) * state.count('#')

        print(result)


print(f"{timeit.timeit(run, number=1)} sec")

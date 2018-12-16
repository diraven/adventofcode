"""
--- Part Two ---

As you're about to begin construction, four of the Elves offer to help. "The sun will set soon; it'll go faster if we work together." Now, you need to account for multiple people working on steps simultaneously. If multiple steps are available, workers should still begin them in alphabetical order.

Each step takes 60 seconds plus an amount corresponding to its letter: A=1, B=2, C=3, and so on. So, step A takes 60+1=61 seconds, while step Z takes 60+26=86 seconds. No time is required between steps.

To simplify things for the example, however, suppose you only have help from one Elf (a total of two workers) and that each step takes 60 fewer seconds (so that step A takes 1 second and step Z takes 26 seconds). Then, using the same instructions as above, this is how each second would be spent:

Second   Worker 1   Worker 2   Done
   0        C          .
   1        C          .
   2        C          .
   3        A          F       C
   4        B          F       CA
   5        B          F       CA
   6        D          F       CAB
   7        D          F       CAB
   8        D          F       CAB
   9        D          .       CABF
  10        E          .       CABFD
  11        E          .       CABFD
  12        E          .       CABFD
  13        E          .       CABFD
  14        E          .       CABFD
  15        .          .       CABFDE

Each row represents one second of time. The Second column identifies how many seconds have passed as of the beginning of that second. Each worker column shows the step that worker is currently doing (or . if they are idle). The Done column shows completed steps.

Note that the order of the steps has changed; this is because steps now take time to finish and multiple workers can begin multiple steps simultaneously.

In this example, it would take 15 seconds for two workers to complete these steps.

With 5 workers and the 60+ second step durations described above, how long will it take to complete all of the steps?
"""
import string
import timeit
from typing import List, Tuple, Dict, Set

Requirements = List[Tuple[str, str]]


def find_available(all_steps: Set[str], requirements: Requirements,
                   steps_done: List[str]):
    """
    Finds what steps are possible to do at the current stage.
    """
    steps = list(all_steps)

    # Exclude steps for which requirements are not yet done.
    for required, requires in requirements:
        try:
            if required not in steps_done:
                steps.remove(requires)
        except ValueError:
            pass

    # Exclude steps that were already done.
    available_steps = [step for step in steps if
                       step not in steps_done]

    # Sort the results.
    available_steps = sorted(available_steps)

    return available_steps


def run() -> None:
    """
    Main function.
    """
    with open("./input.txt") as f:
        data = f.read().splitlines()
        requirements = []  # type: Requirements
        for row in data:
            splitted = row.split()
            requirements.append((splitted[1], splitted[7]))

    all_steps = set()
    for req in requirements:
        all_steps.add(req[0])
        all_steps.add(req[1])

    steps_timings = {}  # type: Dict[str, int]
    for idx, step in enumerate(string.ascii_uppercase):
        steps_timings[step] = 60 + idx + 1

    steps_done = []
    available_steps = find_available(all_steps, requirements, steps_done)

    working = {}  # type: Dict[str, int]
    workers_count = 4
    seconds_elapsed = 0
    # While we have someone still working or steps available.
    while working or available_steps:
        # Clean up work that was finished.
        for step_worked_on, time_left in working.copy().items():
            if time_left == 0:
                steps_done.append(step_worked_on)
                del working[step_worked_on]

        # Recheck work available.
        available_steps = find_available(all_steps, requirements, steps_done)

        # Remove work in progress from available steps.
        for step_worked, time in working.copy().items():
            available_steps.remove(step_worked)

        # Check if we got any idle workers:
        if len(working) < workers_count:
            for i in range(workers_count - len(working)):
                # Check if we have work to do.
                if available_steps:
                    next_step = available_steps.pop(0)
                    working[next_step] = steps_timings[next_step]

        # Now perform 1 frame of work.
        for step_being_worked_on, time_left in working.items():
            working[step_being_worked_on] -= 1

        # Increment time counter.
        seconds_elapsed += 1

    print(seconds_elapsed - 1)


print(timeit.timeit(run, number=1))

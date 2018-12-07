"""
--- Part Two ---

Time to improve the polymer.

One of the unit types is causing problems; it's preventing the polymer from collapsing as much as it should. Your goal is to figure out which unit type is causing the most problems, remove all instances of it (regardless of polarity), fully react the remaining polymer, and measure its length.

For example, again using the polymer dabAcCaCBAcCcaDA from above:

    Removing all A/a units produces dbcCCBcCcD. Fully reacting this polymer produces dbCBcD, which has length 6.
    Removing all B/b units produces daAcCaCAcCcaDA. Fully reacting this polymer produces daCAcaDA, which has length 8.
    Removing all C/c units produces dabAaBAaDA. Fully reacting this polymer produces daDA, which has length 4.
    Removing all D/d units produces abAcCaCBAcCcaA. Fully reacting this polymer produces abCBAc, which has length 6.

In this example, removing all C/c units was best, producing the answer 4.

What is the length of the shortest polymer you can produce by removing all units of exactly one type and fully reacting the result?
"""

import re
import string
import timeit


def run() -> None:
    """
    Main function.
    """
    reacting_combinations = [x + x.upper() for x in string.ascii_lowercase] + \
                            [x.upper() + x for x in string.ascii_lowercase]
    re_text = f'(?:{"|".join(reacting_combinations)})+'
    rexp = re.compile(re_text)

    with open("./input.txt") as f:
        data = f.read()

        # Reduce original polymer.
        n = 1
        while n > 0:
            data, n = re.subn(rexp, "", data)

        # Try removing units one by one and reduce the resulting polymer.
        removed_unit = ""
        minimum_size = len(data)
        for char in string.ascii_lowercase:
            print(char)

            data_without_char = re.sub(char, "", data, flags=re.IGNORECASE)
            print(data_without_char)

            n = 1
            while n > 0:
                data_without_char, n = re.subn(rexp, "", data_without_char)

            print(len(data_without_char))

            if len(data_without_char) < minimum_size:
                minimum_size = len(data_without_char.strip())
                removed_unit = char

        print(removed_unit)
        print(minimum_size)


print(timeit.timeit(run, number=1))

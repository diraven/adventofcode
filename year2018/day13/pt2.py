"""
There isn't much you can do to prevent crashes in this ridiculous system. However, by predicting the crashes, the Elves know where to be in advance and instantly remove the two crashing carts the moment any crash occurs.

They can proceed like this for a while, but eventually, they're going to run out of carts. It could be useful to figure out where the last cart that hasn't crashed will end up.

For example:

/>-<\
|   |
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/

/---\
|   |
| v-+-\
| | | |
\-+-/ |
  |   |
  ^---^

/---\
|   |
| /-+-\
| v | |
\-+-/ |
  ^   ^
  \---/

/---\
|   |
| /-+-\
| | | |
\-+-/ ^
  |   |
  \---/

After four very expensive crashes, a tick ends with only one cart remaining; its final location is 6,4.

What is the location of the last cart at the end of the first tick where it is the only cart left?
"""
import timeit
from collections import deque
from typing import List, Optional, Dict, Tuple

import numpy as np


def direction_left(orig_direction: str) -> str:
    if orig_direction == '^':
        return '<'
    if orig_direction == '>':
        return '^'
    if orig_direction == 'v':
        return '>'
    if orig_direction == '<':
        return 'v'


def direction_straight(orig_direction: str) -> str:
    return orig_direction


def direction_right(orig_direction: str) -> str:
    if orig_direction == '^':
        return '>'
    if orig_direction == '>':
        return 'v'
    if orig_direction == 'v':
        return '<'
    if orig_direction == '<':
        return '^'


class Grid:
    def __init__(self, data: str):
        data = data.splitlines()

        self.grid = []  # type: List[List[Optional[Cell]]]
        for x, col in enumerate(
                np.array([list(row) for row in data]).transpose()):
            if x not in self.grid:
                self.grid.append([])
            for y, cell in enumerate(col):
                if cell.strip():
                    self.grid[x].append(Cell(x, y, cell))
                else:
                    self.grid[x].append(None)

        for x, col in enumerate(self.grid):
            for y, cell in enumerate(col):
                if cell:
                    if str(cell.encoded_type) == "|":
                        cell.exits['^'] = self.grid[x][y - 1]
                        cell.exits['v'] = self.grid[x][y + 1]
                    if str(cell.encoded_type) == "-":
                        cell.exits['>'] = self.grid[x + 1][y]
                        cell.exits['<'] = self.grid[x - 1][y]

                    if str(cell.encoded_type) == "/":
                        if x > 0 and self.grid[x - 1][y] \
                                and self.grid[x - 1][y].encoded_type in "-+":
                            cell.exits['<'] = self.grid[x - 1][y]
                            cell.exits['^'] = self.grid[x][y - 1]
                        else:
                            cell.exits['>'] = self.grid[x + 1][y]
                            cell.exits['v'] = self.grid[x][y + 1]

                    if str(cell.encoded_type) == "\\":
                        if x > 0 and self.grid[x - 1][y] \
                                and self.grid[x - 1][y].encoded_type in "-+":
                            # Top edge, right edge and corner.
                            cell.exits['<'] = self.grid[x - 1][y]
                            cell.exits['v'] = self.grid[x][y + 1]
                        else:
                            # Everything else.
                            cell.exits['>'] = self.grid[x + 1][y]
                            cell.exits['^'] = self.grid[x][y - 1]

                    if str(cell.encoded_type) == "+":
                        cell.exits['^'] = self.grid[x][y - 1]
                        cell.exits['>'] = self.grid[x + 1][y]
                        cell.exits['v'] = self.grid[x][y + 1]
                        cell.exits['<'] = self.grid[x - 1][y]

    def tick(self) -> Optional[Tuple[int, int]]:
        carts_moved = []

        for x, col in enumerate(self.grid):
            for y, cell in enumerate(col):
                if cell and cell.cart:
                    if cell.cart in carts_moved:
                        continue
                    else:
                        carts_moved.append(cell.cart)

                    cart = cell.cart
                    new_cell = cell.exits[cart.direction]  # type: Cell
                    if new_cell.cart:
                        # Remove carts.
                        try:
                            carts_moved.remove(cell.cart)
                            carts_moved.remove(new_cell.cart)
                        except ValueError:
                            pass
                        cell.cart = None
                        new_cell.cart = None
                        continue

                    # Calculate new cart direction.
                    if new_cell.encoded_type == "/":
                        if cart.direction == "^":
                            cart.direction = ">"
                        elif cart.direction == ">":
                            cart.direction = "^"
                        elif cart.direction == "v":
                            cart.direction = "<"
                        elif cart.direction == "<":
                            cart.direction = "v"

                    if new_cell.encoded_type == "\\":
                        if cart.direction == "^":
                            cart.direction = "<"
                        elif cart.direction == ">":
                            cart.direction = "v"
                        elif cart.direction == "v":
                            cart.direction = ">"
                        elif cart.direction == "<":
                            cart.direction = "^"

                    if new_cell.encoded_type == "+":
                        cart.direction = cart.turns[0](cart.direction)
                        cart.turns.rotate(-1)

                    # Actually move cart to a new position.
                    cell.cart = None
                    new_cell.cart = cart
                    cart.cell = new_cell

        if len(carts_moved) == 1:
            return carts_moved[0].cell.x, carts_moved[0].cell.y

    def __str__(self) -> str:
        data = [[str(cell or " ") for cell in col] for col in self.grid]
        data = np.array(data).transpose()

        result = ""
        for row in data:
            for cell in row:
                if cell:
                    result += cell
                else:
                    result += " "
            result += "\n"

        return result

    def __repr__(self) -> str:
        return self.__str__()


class Cell:
    def __init__(self, x, y, encoded_type: str):
        self.x = x
        self.y = y

        self.encoded_type = encoded_type

        self.exits = {}  # type: Dict[str, Cell]

        if encoded_type == "|":
            pass
        if encoded_type == "-":
            pass
        if encoded_type == "/":
            pass
        if encoded_type == "\\":
            pass
        if encoded_type == "+":
            pass

        self.cart = None
        if encoded_type == "^":
            self.encoded_type = "|"
            self.cart = Cart(self, encoded_type)
        if encoded_type == ">":
            self.encoded_type = "-"
            self.cart = Cart(self, encoded_type)
        if encoded_type == "v":
            self.encoded_type = "|"
            self.cart = Cart(self, encoded_type)
        if encoded_type == "<":
            self.encoded_type = "-"
            self.cart = Cart(self, encoded_type)

        self.exits = {}

    def __str__(self) -> str:
        if self.cart:
            return str(self.cart)
        return self.encoded_type

    def __repr__(self) -> str:
        return self.__str__()


class Cart:
    def __init__(self, cell: Cell, encoded: str):
        self.direction = encoded
        self.cell = cell

        self.turns = deque(
            [direction_left, direction_straight, direction_right]
        )

    def __str__(self) -> str:
        return self.direction

    def __repr__(self) -> str:
        return self.__str__()


def run() -> None:
    """
    Main function.
    """
    with open("./input.txt") as f:
        # Load data.
        grid = Grid(f.read())

        counter = 0
        while True:
            counter += 1
            cart_left = grid.tick()
            if cart_left:
                print(cart_left)
                break


print(f"{timeit.timeit(run, number=1)} sec")

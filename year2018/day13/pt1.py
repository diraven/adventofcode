"""
--- Day 13: Mine Cart Madness ---

A crop of this size requires significant logistics to transport produce,
soil, fertilizer, and so on. The Elves are very busy pushing things around
in carts on some kind of rudimentary system of tracks they've come up with.

Seeing as how cart-and-track systems don't appear in recorded history for
another 1000 years, the Elves seem to be making this up as they go along.
They haven't even figured out how to avoid collisions yet.

You map out the tracks (your puzzle input) and see where you can help.

Tracks consist of straight paths (| and -), curves (/ and \),
and intersections (+). Curves connect exactly two perpendicular pieces of
track; for example, this is a closed loop:

/----\
|    |
|    |
\----/

Intersections occur when two perpendicular paths cross. At an intersection,
a cart is capable of turning left, turning right, or continuing straight.
Here are two loops connected by two intersections:

/-----\
|     |
|  /--+--\
|  |  |  |
\--+--/  |
   |     |
   \-----/

Several carts are also on the tracks. Carts always face either up (^),
down (v), left (<), or right (>). (On your initial map, the track under each
cart is a straight path matching the direction the cart is facing.)

Each time a cart has the option to turn (by arriving at any intersection),
it turns left the first time, goes straight the second time, turns right the
third time, and then repeats those directions starting again with left the
fourth time, straight the fifth time, and so on. This process is independent
of the particular intersection at which the cart has arrived - that is,
the cart has no per-intersection memory.

Carts all move at the same speed; they take turns moving a single step at a
time. They do this based on their current location: carts on the top row
move first (acting from left to right), then carts on the second row move (
again from left to right), then carts on the third row, and so on. Once each
cart has moved one step, the process repeats; each of these loops is called
a tick.

For example, suppose there are two carts on a straight track:

|  |  |  |  |
v  |  |  |  |
|  v  v  |  |
|  |  |  v  X
|  |  ^  ^  |
^  ^  |  |  |
|  |  |  |  |

First, the top cart moves. It is facing down (v), so it moves down one
square. Second, the bottom cart moves. It is facing up (^), so it moves up
one square. Because all carts have moved, the first tick ends. Then,
the process repeats, starting with the first cart. The first cart moves
down, then the second cart moves up - right into the first cart, colliding
with it! (The location of the crash is marked with an X.) This ends the
second and last tick.

Here is a longer example:

/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/

/-->\
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \->--/
  \------/

/---v
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+>-/
  \------/

/---\
|   v  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+->/
  \------/

/---\
|   |  /----\
| /->--+-\  |
| | |  | |  |
\-+-/  \-+--^
  \------/

/---\
|   |  /----\
| /-+>-+-\  |
| | |  | |  ^
\-+-/  \-+--/
  \------/

/---\
|   |  /----\
| /-+->+-\  ^
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /----<
| /-+-->-\  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /---<\
| /-+--+>\  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /--<-\
| /-+--+-v  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /-<--\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/

/---\
|   |  /<---\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-<--/
  \------/

/---\
|   |  v----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \<+--/
  \------/

/---\
|   |  /----\
| /-+--v-\  |
| | |  | |  |
\-+-/  ^-+--/
  \------/

/---\
|   |  /----\
| /-+--+-\  |
| | |  X |  |
\-+-/  \-+--/
  \------/

After following their respective paths for a while, the carts eventually crash.
 To help prevent crashes, you'd like to know the location of the first crash.
 Locations are given in X,Y coordinates, where the furthest left column is X=0
 and the furthest top row is Y=0:

           111
 0123456789012
0/---\
1|   |  /----\
2| /-+--+-\  |
3| | |  X |  |
4\-+-/  \-+--/
5  \------/

In this example, the location of the first crash is 7,3.
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
                        return new_cell.x, new_cell.y

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
            collision = grid.tick()
            if collision:
                print(collision)
                break


print(f"{timeit.timeit(run, number=1)} sec")

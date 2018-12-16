from typing import List, Optional

from .cell import Cell
from .creature import Creature
from .elf import Elf
from .goblin import Goblin
from .wall import Wall


class Grid:
    def __init__(self, data: str):
        self.grid = []
        self.casualties = 0

        for row_num, row in enumerate(data.splitlines()):
            self.grid.append([])
            for col_num, char in enumerate(row):
                cell = Cell(self, row_num, col_num)
                if char == "#":
                    cell.content = Wall()
                if char == ".":
                    cell.content = None
                if char == "E":
                    cell.content = Elf(cell, Goblin)
                if char == "G":
                    cell.content = Goblin(cell, Elf)
                self.grid[row_num].append(cell)

    def get_turns_order(self) -> List[Creature]:
        result = []
        for row in self.grid:
            for cell in row:
                if isinstance(cell.content, Creature):
                    result.append(cell.content)
        return result

    def tick(self) -> Optional[Creature]:
        turns_order = self.get_turns_order()
        for creature in turns_order:
            if creature.alive:
                last_actor = creature.act()
                if last_actor:
                    return last_actor

    def find_all(self, klass) -> List[Cell]:
        result = []
        for row in self.grid:
            for cell in row:
                if isinstance(cell.content, klass):
                    result.append(cell)
        return result

    def __str__(self) -> str:
        result = []
        for row_num, row in enumerate(self.grid):
            result.append([])
            for cell in row:
                result[row_num].append(str(cell))
            for cell in row:
                if isinstance(cell.content, Creature):
                    result[row_num].append(" " + repr(cell.content))

        return "\n".join(
            ["".join([str(cell) for cell in row]) for row in result]
        )

    def encoded(self) -> List[List[int]]:
        result = []
        for row_num, row in enumerate(self.grid):
            result.append([])
            for cell in row:
                result[row_num].append(cell.encoded())

        return result

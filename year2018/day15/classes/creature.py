from functools import total_ordering
from typing import Optional, List

from pathfinding.core.grid import Grid
from pathfinding.finder.breadth_first import BreadthFirstFinder

from .cell import Cell

finder = BreadthFirstFinder()


@total_ordering
class Creature:
    name = '?'
    hp = 200
    ap = 3

    def __init__(self, cell: Cell, enemy_class):
        self.cell = cell
        self.enemy = enemy_class

    def __lt__(self, other) -> bool:
        return (self.cell.row, self.cell.col) < (
            other.cell.row, other.cell.col)

    def __eq__(self, other) -> bool:
        return (self.cell.row, self.cell.col) == (
            other.cell.row, other.cell.col)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{self.name}@({self.cell.row}, {self.cell.col})({self.hp}hp)"

    @property
    def alive(self) -> bool:
        return self.hp > 0

    def act(self) -> Optional['Creature']:
        enemies_in_reach = [cell.content for cell in self.cell.get_neighbours()
                            if isinstance(cell.content, self.enemy)]
        if enemies_in_reach:
            enemies_in_reach.sort(key=lambda x: (x.hp, x.cell.row, x.cell.col))
            self.attack(enemies_in_reach[0])
            return

        enemy_locations = self.cell.grid.find_all(self.enemy)
        if enemy_locations:
            self.go(enemy_locations)
            enemies_in_reach = [cell.content for cell in
                                self.cell.get_neighbours()
                                if isinstance(cell.content, self.enemy)]
            if enemies_in_reach:
                enemies_in_reach.sort(
                    key=lambda x: (x.hp, x.cell.row, x.cell.col))
                self.attack(enemies_in_reach[0])

            return

        # No actions taken, nothing to do, return last actor.
        return self

    def attack(self, target_creature: 'Creature'):
        # print(f"{repr(self)}: attacking {repr(target_creature)}")
        target_creature.hp -= self.ap
        if not target_creature.alive:
            target_creature.cell.content = None

    def go(self, enemy_locations: List[Cell]) -> None:
        grid = Grid(matrix=self.cell.grid.encoded())
        destinations = []
        for location in enemy_locations:
            destinations += location.get_empty_neighbours()
        paths = []
        for cell in destinations:
            for neighbour in self.cell.get_empty_neighbours():
                grid.cleanup()
                start = grid.node(neighbour.col, neighbour.row)
                end = grid.node(cell.col, cell.row)
                path, _ = finder.find_path(start, end, grid)
                if path:
                    paths.append(path)

        paths.sort(
            key=lambda x: (len(x), x[-1][1], x[-1][0], x[0][1], x[0][0])
        )

        try:
            go_row = paths[0][0][1]
            go_col = paths[0][0][0]
            dest = self.cell.grid.grid[go_row][go_col]

            # print(f"{repr(self)}: going to {repr(dest)}")

            self.cell.content = None
            self.cell = dest
            dest.content = self

        except IndexError:
            pass
            # print(f"{repr(self)}: nowhere to go!")

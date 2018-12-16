from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .grid import Grid


class Cell:
    def __init__(self, grid: 'Grid', row: int, col: int):
        self.grid = grid
        self.content = None

        if self.content:
            self.content.cell = self
        self.row = row
        self.col = col

    def encoded(self):
        if not self.content:
            return 1
        return self.content.encoded

    def __str__(self) -> str:
        return str(self.content or ".")

    def __repr__(self) -> str:
        return f"Cell@({self.row}, {self.col})"

    def get_neighbours(self) -> List['Cell']:
        neighbours = []
        # North.
        cell = self.grid.grid[self.row - 1][self.col]
        if self.row != 0:
            neighbours.append(cell)

        # West.
        cell = self.grid.grid[self.row][self.col - 1]
        if self.row != 0:
            neighbours.append(cell)

        # East.
        cell = self.grid.grid[self.row][self.col + 1]
        if self.row != 0:
            neighbours.append(cell)

        # South.
        cell = self.grid.grid[self.row + 1][self.col]
        if self.row != 0:
            neighbours.append(cell)

        return neighbours

    def get_empty_neighbours(self) -> List['Cell']:
        return [cell for cell in self.get_neighbours() if cell.content is None]

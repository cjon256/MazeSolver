from typing import Optional, Any, Callable
from geometry import CellLocation
from dataclasses import dataclass
from enum import Enum

@dataclass(kw_only=True)
class VCWGridLoc:
    row: int
    col: int

class VCWGrid:
    def __init__(self, cell_rows: int, cell_cols: int) -> None:
        self.cell_rows = cell_rows
        self.cell_cols = cell_cols
        self._grid = self._create_vertex_cell_wall_grid()

    def _create_vertex_cell_wall_grid(self) -> list[Any]:
        """creates a grid that is 2x+1 in both dimensions"""
        self._row_length = 2 * self.cell_rows + 1
        self._col_length = 2 * self.cell_cols + 1
        return [[None for _ in range(self._col_length)] for _ in range(self._row_length)]

    def cells_locs(self) -> iter:
        for row in range(self.cell_rows):
            for col in range(self.cell_cols):
                yield CellLocation(row=row, col=col)

    def map_cells(self, func: Callable[[Any], Any]) -> iter:
        for row in range(1, self._row_length, 2):
            for col in range(1, self._col_length, 2):
                func(self._grid[row][col])

    def map_walls(self, func: Callable[[Any], Any]):
        for row in range(0, self._row_length, 1):
            if row % 2 == 1:
                for col in range(0, self._col_length, 2):
                    func(self._grid[row][col])
            else:
                for col in range(1, self._col_length, 2):
                    func(self._grid[row][col])

    def populate_walls(self, func: Callable[[VCWGridLoc], Any]):
        for row in range(0, self._row_length, 2):
            for col in range(1, self._col_length, 2):
                self._grid[row][col] = func(VCWGridLoc(row=row, col=col))
        for row in range(1, self._row_length, 2):
            for col in range(0, self._col_length, 2):
                self._grid[row][col] = func(VCWGridLoc(row=row, col=col))

    def scale_location(loc: CellLocation) -> tuple[int, int]:
        grid_row = 2 * loc.row + 1
        grid_col = 2 * loc.col + 1
        return grid_row,grid_col

    def is_valid_cell(self, row: int, col: int) -> bool:
        return (col >= 0 and col <= self.cell_cols 
                and row >= 0 and row <= self.cell_rows)

    def get_cell(self, loc: CellLocation) -> Any:
        if not self.is_valid_cell(row=loc.row, col=loc.col):
            raise Exception(f"Cell index out of range {loc}")
        grid_row, grid_col = VCWGrid.scale_location(loc)
        return self._grid[grid_row][grid_col]

    def set_cell(self, loc: CellLocation, val: Any) -> None:
        if not self.is_valid_cell(row=loc.row, col=loc.col):
            raise Exception(f"Cell index out of range {loc}")
        grid_row, grid_col = VCWGrid.scale_location(loc)
        self._grid[grid_row][grid_col] = val

    def get_north_wall(self, loc: CellLocation) -> Any:
        cell_row, cell_col = VCWGrid.scale_location(loc)
        return self._grid[cell_row-1][cell_col]

    def get_south_wall(self, loc: CellLocation) -> Any:
        cell_row, cell_col = VCWGrid.scale_location(loc)
        return self._grid[cell_row+1][cell_col]

    def get_east_wall(self, loc: CellLocation) -> Any:
        cell_row, cell_col = VCWGrid.scale_location(loc)
        return self._grid[cell_row][cell_col+1]

    def get_west_wall(self, loc: CellLocation) -> Any:
        cell_row, cell_col = VCWGrid.scale_location(loc)
        return self._grid[cell_row][cell_col-1]

    def get_adjacent_cell_locations(self, 
                                    loc: CellLocation) -> list[CellLocation]:
        neigh = []
        if loc.row > 0:
            north_loc = CellLocation(row=loc.row-1, col=loc.col)
            neigh.append(north_loc)
        if loc.row < self.cell_rows-1:
            south_loc = CellLocation(row=loc.row+1, col=loc.col)
            neigh.append(south_loc)
        if loc.col < self.cell_cols-1:
            east_loc = CellLocation(row=loc.row, col=loc.col+1)
            neigh.append(east_loc)
        if loc.col > 0:
            west_loc = CellLocation(row=loc.row, col=loc.col-1)
            neigh.append(west_loc)
        return neigh


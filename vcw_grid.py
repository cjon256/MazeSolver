from typing import Optional, Any, Callable
from geometry import Location

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

    def vertices(self) -> iter:
        for row in range(0, self._row_length, 2):
            for col in range(0, self._col_length, 2):
                yield self._grid[row][col]
    vertexes = vertices # two possible plurals

    def cells(self) -> iter:
        for row in range(1, self._row_length, 2):
            for col in range(1, self._col_length, 2):
                yield self._grid[row][col]

    def walls(self) -> iter:
        for row in range(0, self._row_length, 1):
            if row % 2 == 1:
                for col in range(0, self._col_length, 2):
                    yield self._grid[row][col]
            else:
                for col in range(1, self._col_length, 2):
                    yield self._grid[row][col]

    def apply_to_vertices(self, func: Callable[[Any], Any]) -> iter:
        for row in range(0, self._row_length, 2):
            for col in range(0, self._col_length, 2):
                self._grid[row][col] = func(self._grid[row][col])
    apply_to_vertexes = apply_to_vertices # two possible plurals

    def apply_to_cells(self, func: Callable[[Any], Any]) -> iter:
        for row in range(1, self._row_length, 2):
            for col in range(1, self._col_length, 2):
                self._grid[row][col] = func(self._grid[row][col])


    def apply_to_walls(self, func: Callable[[Any], Any]):
        for row in range(0, self._row_length, 1):
            if row % 2 == 1:
                for col in range(0, self._col_length, 2):
                    self._grid[row][col] = func(self._grid[row][col])
            else:
                for col in range(1, self._col_length, 2):
                    self._grid[row][col] = func(self._grid[row][col])

    def map_walls(self, func: Callable[[Any], Any]):
        for row in range(0, self._row_length, 1):
            if row % 2 == 1:
                for col in range(0, self._col_length, 2):
                    func(self._grid[row][col])
            else:
                for col in range(1, self._col_length, 2):
                    func(self._grid[row][col])

    def populate_cells(self, func: Callable[[Any], Any]):
        for row in range(1, self._row_length, 2):
            for col in range(1, self._col_length, 2):
                self._grid[row][col] = func(row, col)
        pass

    def populate_horz_walls(self, func: Callable[[Any], Any]):
        for row in range(0, self._row_length, 2):
            for col in range(1, self._col_length, 2):
                self._grid[row][col] = func(row,col)

    def populate_vert_walls(self, func: Callable[[Any], Any]):
        for row in range(1, self._row_length, 2):
            for col in range(0, self._col_length, 2):
                self._grid[row][col] = func(row,col)

    def scale_location(loc: Location) -> tuple[int, int]:
        grid_row = 2 * loc.row + 1
        grid_col = 2 * loc.col + 1
        return grid_row,grid_col

    def is_valid_cell(self, row: int, col: int) -> bool:
        return (col >= 0 and col <= self.cell_cols and row >= 0 and row <= self.cell_rows)

    def get_cell(self, loc: Location) -> Any:
        if not self.is_valid_cell(row=loc.row, col=loc.col):
            print(loc)
            raise Exception(f"Cell index out of range {loc}")
        grid_row, grid_col = VCWGrid.scale_location(loc)
        return self._grid[grid_row][grid_col]

    def get_north_wall(self, loc: Location) -> Any:
        cell_row, cell_col = VCWGrid.scale_location(loc)
        return self._grid[cell_row-1][cell_col]

    def get_south_wall(self, loc: Location) -> Any:
        cell_row, cell_col = VCWGrid.scale_location(loc)
        return self._grid[cell_row+1][cell_col]

    def get_east_wall(self, loc: Location) -> Any:
        cell_row, cell_col = VCWGrid.scale_location(loc)
        return self._grid[cell_row][cell_col+1]

    def get_west_wall(self, loc: Location) -> Any:
        cell_row, cell_col = VCWGrid.scale_location(loc)
        return self._grid[cell_row][cell_col-1]

    @property
    def grid(self):
        return self._grid

    def get_cell_to_north(self, loc: Location):
        cell_row, cell_col = VCWGrid.scale_location(loc)
        return self._grid[cell_row-2][cell_col]

    def get_cell_to_south(self, loc: Location):
        cell_row, cell_col = VCWGrid.scale_location(loc)
        return self._grid[cell_row+2][cell_col]

    def get_cell_to_east(self, loc: Location):
        cell_row, cell_col = VCWGrid.scale_location(loc)
        return self._grid[cell_row][cell_col+2]

    def get_cell_to_west(self, loc: Location):
        cell_row, cell_col = VCWGrid.scale_location(loc)
        return self._grid[cell_row][cell_col-2]

    def get_adjacent_cell_locations(self, loc: Location) -> list[Location]:
        neigh = []
        if loc.row > 0:
            north_loc = Location(loc.row-1, loc.col)
            # print(f"appending location {north_loc=}")
            neigh.append(north_loc)
        if loc.row < self.cell_rows-1:
            south_loc = Location(loc.row+1, loc.col)
            # print(f"appending location {south_loc}")
            neigh.append(south_loc)
        if loc.col < self.cell_cols-1:
            east_loc = Location(loc.row, loc.col+1)
            # print(f"appending location {east_loc}")
            neigh.append(east_loc)
        if loc.col > 0:
            west_loc = Location(loc.row, loc.col-1)
            # print(f"appending location {west_loc}")
            neigh.append(west_loc)
        return neigh

    def get_adjacent_cells(self, loc: Location) -> list[Any]:
        neigh = []
        if loc.col > 0:
            neigh.append(self.get_cell_to_north(loc))
        if loc.col < self.cell_cols-1:
            neigh.append(self.get_cell_to_south(loc))
        if loc.row < self.cell_rows-1:
            neigh.append(self.get_cell_to_east(loc))
        if loc.row > 0:
            neigh.append(self.get_cell_to_west(loc))
        return neigh




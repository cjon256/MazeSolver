
    # def vertices(self) -> iter:
    #     for row in range(0, self._row_length, 2):
    #         for col in range(0, self._col_length, 2):
    #             yield self._grid[row][col]
    # vertexes = vertices # two possible plurals


    # def cells(self) -> iter:
    #     for row in range(1, self._row_length, 2):
    #         for col in range(1, self._col_length, 2):
    #             yield self._grid[row][col]

    # def walls(self) -> iter:
    #     for row in range(0, self._row_length, 1):
    #         if row % 2 == 1:
    #             for col in range(0, self._col_length, 2):
    #                 yield self._grid[row][col]
    #         else:
    #             for col in range(1, self._col_length, 2):
    #                 yield self._grid[row][col]

    # def apply_to_vertices(self, func: Callable[[Any], Any]) -> iter:
    #     for row in range(0, self._row_length, 2):
    #         for col in range(0, self._col_length, 2):
    #             self._grid[row][col] = func(self._grid[row][col])
    # apply_to_vertexes = apply_to_vertices # two possible plurals
    #
    # def apply_to_cells(self, func: Callable[[Any], Any]) -> iter:
    #     for row in range(1, self._row_length, 2):
    #         for col in range(1, self._col_length, 2):
    #             self._grid[row][col] = func(self._grid[row][col])


    # def apply_to_walls(self, func: Callable[[Any], Any]):
    #     for row in range(0, self._row_length, 1):
    #         if row % 2 == 1:
    #             for col in range(0, self._col_length, 2):
    #                 self._grid[row][col] = func(self._grid[row][col])
    #         else:
    #             for col in range(1, self._col_length, 2):
    #                 self._grid[row][col] = func(self._grid[row][col])
    #
    # def map_vertices(self, func: Callable[[Any], Any]) -> iter:
    #     for row in range(0, self._row_length, 2):
    #         for col in range(0, self._col_length, 2):
    #             func(self._grid[row][col])
    # map_vertexes = map_vertices # two possible plurals


    # def populate_vertexes(self, func: Callable[[Any], Any]):
    #     for row in range(0, self._row_length, 2):
    #         for col in range(0, self._col_length, 2):
    #             self._grid[row][col] = func(row, col)
    # populate_vertices = populate_vertexes
    #
    # def populate_cells(self, func: Callable[[Any], Any]):
    #     for row in range(1, self._row_length, 2):
    #         for col in range(1, self._col_length, 2):
    #             self._grid[row][col] = func(row, col)


    # def populate_horz_walls(self, func: Callable[[Any], Any]):
    #     for row in range(0, self._row_length, 2):
    #         for col in range(1, self._col_length, 2):
    #             self._grid[row][col] = func(row,col)
    #
    # def populate_vert_walls(self, func: Callable[[Any], Any]):
    #     for row in range(1, self._row_length, 2):
    #         for col in range(0, self._col_length, 2):
    #             self._grid[row][col] = func(row,col)


    # def get_cell_to_north(self, loc: CellLocation):
    #     cell_row, cell_col = VCWGrid.scale_location(loc)
    #     return self._grid[cell_row-2][cell_col]
    #
    # def get_cell_to_south(self, loc: CellLocation):
    #     cell_row, cell_col = VCWGrid.scale_location(loc)
    #     return self._grid[cell_row+2][cell_col]
    #
    # def get_cell_to_east(self, loc: CellLocation):
    #     cell_row, cell_col = VCWGrid.scale_location(loc)
    #     return self._grid[cell_row][cell_col+2]
    #
    # def get_cell_to_west(self, loc: CellLocation):
    #     cell_row, cell_col = VCWGrid.scale_location(loc)
    #     return self._grid[cell_row][cell_col-2]

    # def get_adjacent_cells(self, loc: CellLocation) -> list[Any]:
    #     neigh = []
    #     if loc.col > 0:
    #         neigh.append(self.get_cell_to_north(loc))
    #     if loc.col < self.cell_cols-1:
    #         neigh.append(self.get_cell_to_south(loc))
    #     if loc.row < self.cell_rows-1:
    #         neigh.append(self.get_cell_to_east(loc))
    #     if loc.row > 0:
    #         neigh.append(self.get_cell_to_west(loc))
    #     return neigh


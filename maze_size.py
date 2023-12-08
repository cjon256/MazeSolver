from dataclasses import dataclass

@dataclass(frozen=True)
class MazeSize:
    """RowsAndCols keeps track of how many rows and columns of each type there are"""
    cell_rows: int
    cell_cols: int

    @property
    def vertex_rows(self):
        return self.cell_rows + 1

    @property
    def vertex_cols(self):
        return self.cell_cols + 1

    @property
    def horz_wall_rows(self):
        return self.cell_rows + 1

    @property
    def horz_wall_cols(self):
        return self.cell_cols

    @property
    def vert_wall_rows(self):
        return self.cell_rows

    @property
    def vert_wall_cols(self):
        return self.cell_cols + 1


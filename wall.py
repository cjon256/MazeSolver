from tkinter import Tk, BOTH, Canvas
from typing import Any, Self, Callable, Optional
from itertools import chain

from geometry import Point, Line, Location

class Wall:
    def __init__(self: Self,
                 loc: Location,
                 start: Point,
                 end: Point,
                 solid: bool=True) -> None:
        self.line = Line(start, end)
        self.solid = solid
        self.loc = loc

    def draw(self: Self, renderer: Callable[[Line, str], None], color: Optional[str]=None) -> None:
        if color:
            fillcolor = color
        else:
            fillcolor = "black" if self.solid else "white"
        renderer(self.line, fillcolor)

    def __repr__(self) -> str:
        return f"Wall(loc={self.loc}, line={self.line}, solid={self.solid})"

class Cell:
    def __init__(self: Self, point: Point, visited: bool=False) -> None:
        self.point = point
        self.visited = visited

    def draw(self: Self, renderer: Callable[[Point, str], None], color: Optional[str]=None) -> None:
        renderer(self.point, color)

    def __repr__(self: Self) -> str:
        return f"Cell(visited={self.visited})"

class Path:
    def __init__(self: Self,
                 start: Point,
                 end: Point) -> None:
        self.line = Line(start, end)

    def draw(self: Self, renderer: Callable[[Line, str], None], color: Optional[str]=None) -> None:
        if color:
            fillcolor = color
        else:
            fillcolor = "RoyalBlue1"
        renderer(self.line, fillcolor)

class WallGrid:
    def __init__(self,
                 upper_right_corner: Point,
                 cell_size_x: int,
                 cell_size_y: int,
                 num_rows: int,
                 num_cols: int,
                 ):
        upper_right_corner = upper_right_corner
        self.x1 = upper_right_corner.x
        self.y1 = upper_right_corner.y
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.lr_walls = self.create_leftright_walls()
        self.ud_walls = self.create_updown_walls()
        self.centers = self.create_centers()
        self.vert_paths = self.create_vertical_paths()
        self.horz_paths = self.create_horizontal_paths()

    def printall(self: Self) -> None:
        print(f"WallGrid(lr_walls={self.lr_walls},")
        print(f"         ud_walls={self.ud_walls},")
        print(f"         centers={self.centers})")

    def is_valid_cell(self: Self, row: int, col: int) -> bool:
        return (col >= 0 and col <= self.num_cols and row >= 0 and row <= self.num_rows)

    def is_not_last_row_cell(self: Self, row: int) -> bool:
        return row < self.num_rows

    def create_leftright_walls(self: Self) -> list[Wall]:
        lr_walls = []
        for row in range(self.num_rows):
            lr_wall_row = []
            for col in range(self.num_cols + 1):
                    lr_wall_row.append(Wall(
                        Location(row, col),
                        Point(
                            x = self.x1 + self.cell_size_x * col,
                            y = self.y1 + self.cell_size_y * row
                            ),
                        Point(
                            x = self.x1 + self.cell_size_x * col,
                            y = self.y1 + self.cell_size_y * (row+1)
                            )
                        ))
            lr_walls.append(lr_wall_row)
        return lr_walls

    def create_updown_walls(self: Self) -> list[Wall]:
        ud_walls = []
        for row in range(self.num_rows + 1):
            ud_wall_row = []
            for col in range(self.num_cols):
                ud_wall_row.append(Wall(
                    Location(row, col),
                    Point(
                        x = self.x1 + self.cell_size_x * col,
                        y = self.y1 + self.cell_size_y * row,
                        ),
                    Point(
                        x = self.x1 + self.cell_size_x * (col+1),
                        y = self.y1 + self.cell_size_y * row,
                        )
                    ))
            ud_walls.append(ud_wall_row)
        return ud_walls

    def generate_center_point(self: Self, row: int, col: int) -> Point:
        center_offset_x = self.cell_size_x // 2
        center_offset_y = self.cell_size_y // 2
        return Point(x = self.x1 + self.cell_size_x * col + center_offset_x,
                     y = self.y1 + self.cell_size_y * row + center_offset_y)

    def create_centers(self: Self) -> list[Cell]:
        centers = []
        for row in range(self.num_rows):
            centers_row = []
            for col in range(self.num_cols):
                centers_row.append(Cell(self.generate_center_point(row, col)))
            centers.append(centers_row)
        return centers

    def create_horizontal_paths(self: Self) -> list[Path]:
        paths = []
        center_offset_x = self.cell_size_x // 2
        center_offset_y = self.cell_size_y // 2
        for row in range(self.num_rows):
            paths_row = []
            for col in range(self.num_cols - 1):
                paths_row.append(Path(self.generate_center_point(row=row, col=col),
                                      self.generate_center_point(row=row, col=col+1)))
            paths.append(paths_row)
        return paths

    def create_vertical_paths(self: Self) -> list[Path]:
        paths = []
        center_offset_x = self.cell_size_x // 2
        center_offset_y = self.cell_size_y // 2
        for row in range(self.num_rows - 1):
            paths_row = []
            for col in range(self.num_cols):
                paths_row.append(Path(self.generate_center_point(row=row, col=col),
                                      self.generate_center_point(row=row+1, col=col)
                ))
            paths.append(paths_row)
        return paths

    def draw_walls(self: Self, line_renderer: Callable[[Line, str], None]):
        for row in self.lr_walls:
            for wall in row:
                wall.draw(line_renderer)
        for row in self.ud_walls:
            for wall in row:
                wall.draw(line_renderer, color="green2")

    def test_draw_center_points(self: Self, point_renderer: Callable[[Point, str], None]) -> None:
        for row in self.centers:
            for center in row:
                center.draw(point_renderer)

    def test_draw_all_paths(self: Self, line_renderer: Callable[[Line, str], None]):
        for row in self.vert_paths:
            for path in row:
                path.draw(line_renderer)
        for row in self.horz_paths:
            for path in row:
                path.draw(line_renderer)

    def is_not_first_row_cell(self: Self, row: int) -> bool:
        return row > 0

    def is_not_first_col_cell(self: Self, col: int) -> bool:
        return col > 0

    def is_not_last_col_cell(self: Self, col: int) -> bool:
        return col < self.num_cols

    def is_top_border_wall(self: Self, row: int) -> bool:
        return row == 0

    def is_bottom_border_wall(self: Self, row: int) -> bool:
        return row == self.num_rows

    def is_left_border_wall(self: Self, col: int) -> bool:
        return col == 0

    def is_right_border_wall(self: Self, col: int) -> bool:
        print(f"is_right_border_wall(col={col}) -> == {self.num_cols}")
        return col == self.num_cols




    def create_cell_grid(self) -> None:
        """
        _CREATE_CELL_GRID()
        This method should create a rows x cols size grid of cells
        Cell objects. Once matrix is populated it should call its _draw_cell() method on each Cell.
        """
        all_cells: list[Cell] = []
        for row_number in range(self.num_rows):
            row = []
            for col_number in range(self.num_cols):
                has_left_wall = True
                has_right_wall = True
                has_top_wall = True
                has_bottom_wall = True
                up_left = Point(
                    self.x1 + self.cell_size.x * col_number,
                    self.y1 + self.cell_size.y * row_number
                )
                down_right = Point(
                    self.x1 + self.cell_size.x * (col_number + 1),
                    self.y1 + self.cell_size.y * (row_number + 1)
                )
                new_cell = Cell(has_left_wall, has_right_wall, has_top_wall, has_bottom_wall, up_left, down_right)
                row.append(new_cell)
            all_cells.append(row)
        return all_cells

    def __iter__(self):
        return (self.cells[i][j] for j in range(self.num_cols) for i in range(self.num_rows))



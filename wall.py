from tkinter import Tk, BOTH, Canvas
from typing import Any, Self, Callable, Optional
# import random
# from time import sleep
# from collections import deque as Deque
from itertools import chain

from location import Location
from shapes import Point, Line

class Wall:
    def __init__(self: Self,
                 loc: Location,
                 start: Point,
                 end: Point,
                 solid: bool=True):
        self.line = Line(start, end)
        self.solid = solid
        self.loc = loc

    def draw(self: Self, renderer: Callable[[Line, str], None], color: Optional[str]=None) -> None:
        if color:
            fillcolor = self.color
        else:
            fillcolor = "black" if self.solid else "white"
        renderer(self.line, fillcolor)
        # self.line.draw(canvas, fillcolor)

    def __repr__(self):
        return f"Wall(loc={self.loc}, line={self.line}, solid={self.solid})"

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
        self.lr_walls, self.ud_walls, self.centers = self.create_walls_and_centers()
        self.all_walls = list(chain.from_iterable([*self.lr_walls, *self.ud_walls]))

    def printall(self: Self) -> None:
        print(f"WallGrid(lr_walls={self.lr_walls},")
        print(f"         ud_walls={self.ud_walls},")
        print(f"         centers={self.centers})")

    def is_valid_cell(self: Self, row: int, col: int) -> bool:
        return (col >= 0 and col <= self.num_cols and row >= 0 and row <= self.num_rows)

    def is_not_last_row_cell(self: Self, row: int) -> bool:
        return row < self.num_rows

    def create_walls_and_centers(self: Self) -> None:
        lr_walls = []
        ud_walls = []
        centers = []
        center_offset_x = self.cell_size_x // 2
        center_offset_y = self.cell_size_y // 2
        for row in range(self.num_rows + 1):
            lr_wall_row = []
            ud_wall_row = []
            centers_row = []
            for col in range(self.num_cols + 1):
                if self.is_valid_cell(row, col):
                    centers_row.append(Point(
                        x = self.x1 + self.cell_size_x * col + center_offset_x,
                        y = self.y1 + self.cell_size_y * row + center_offset_y
                    ))
                    print(f"col={col} final ={self.is_right_border_wall(col)}")
                if not self.is_bottom_border_wall(row):
                    lr_wall_row.append(Wall(
                        Location(row, col),
                        Point(
                            x = self.x1 + self.cell_size_x * col + center_offset_x,
                            y = self.y1 + self.cell_size_y * row + center_offset_y
                            ),
                        Point(
                            x = self.x1 + self.cell_size_x * col + center_offset_x,
                            y = self.y1 + self.cell_size_y * (row+1) + center_offset_y
                            )
                        ))
                if not self.is_right_border_wall(col):
                    ud_wall_row.append(Wall(
                        Location(row, col),
                        Point(
                            x = self.x1 + self.cell_size_x * col + center_offset_x,
                            y = self.y1 + self.cell_size_y * row + center_offset_y
                            ),
                        Point(
                            x = self.x1 + self.cell_size_x * (col+1) + center_offset_x,
                            y = self.y1 + self.cell_size_y * row + center_offset_y
                            )
                        ))
            if self.is_not_last_row_cell(row):
                centers.append(centers_row)
            ud_walls.append(ud_wall_row)
            lr_walls.append(lr_wall_row)
        return (lr_walls, ud_walls, centers)

    def draw_walls(self: Self, line_renderer: Callable[[Line, str], None]):
        for wall in self.all_walls:
            print(wall)
            try:
                wall.draw(line_renderer)
            except AttributeError:
                pass

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



from tkinter import Tk, BOTH, Canvas
from typing import Any, Self
import random
from time import sleep
from dataclasses import dataclass

from geometry import Point, Line, CellLocation
from maze_elements import Cell, Vertex, WallPath
from vcw_grid import VCWGrid, VCWGridLoc

@dataclass
class ScreenCoordinatCalculator:
    cell_size_in_pixels: int
    border_width_in_pixels: int

    def __post_init__(self):
        self.half_cell = self.cell_size_in_pixels//2
        self.upper_corner = Point(x=self.border_width_in_pixels, 
                                  y=self.border_width_in_pixels)

    def create_vertex_coordinates(self, vertex_rows: int, vertex_cols: int) -> iter:
        for row in range(vertex_rows):
            for col in range(vertex_cols):
                x_coord = self.upper_corner.x + col * self.cell_size_in_pixels
                y_coord = self.upper_corner.y + row * self.cell_size_in_pixels
                yield Point(x=x_coord, y=y_coord)


    def get_vertex_point(self, loc: CellLocation) -> Point:
            x_coord = self.upper_corner.x + col * self.cell_size_in_pixels
            y_coord = self.upper_corner.y + row * self.cell_size_in_pixels
            return Point(x=x_coord, y=y_coord)


    def cell_center_point(self, loc: CellLocation) -> Point:
        x_coord = ( self.upper_corner.x
                  + loc.col * self.cell_size_in_pixels
                  + self.half_cell
                  + 1)
        y_coord = ( self.upper_corner.y
                  + loc.row * self.cell_size_in_pixels
                  + self.half_cell
                  + 1)
        return Point(x=x_coord, y=y_coord)

    def get_line_for_wall(self, indexes: VCWGridLoc) -> Line:
        if indexes.row % 2 == 0: # horz_wall
            horz_row = indexes.row//2
            horz_start_col = indexes.col//2
            horz_end_col = horz_start_col + 1
            if DEBUG:
                print(f"HW({horz_start_col=},{horz_end_col=}), {horz_row=}")
            return Line(start=self.vertex_grid[horz_row][horz_start_col],
                        end=self.vertex_grid[horz_row][horz_end_col])
        else:
            vert_start_row = indexes.row//2
            vert_end_row = vert_start_row + 1
            vert_col = indexes.col//2
            if DEBUG:
                print(f"VW:({vert_start_row=},{vert_end_row=}),{vert_col=}")
            return Line(start=self.vertex_grid[vert_start_row][vert_col],
                        end=self.vertex_grid[vert_end_row][vert_col])

    def get_line_for_path(self, cell_index: Point) -> Line:
        vert = self.get_vertex_point(*cell_index)
        if indexes.row % 2 == 0: # vert_path
            x        = vert.x + self.half_cell
            first_y  = vert.y - self.half_cell
            second_y = vert.y + self.half_cell
            first_point  = Point(x=x, y=first_y)
            second_point = Point(x=x, y=second_y)
        else:
            first_x  = vert.x - self.half_cell
            second_x = vert.x + self.half_cell
            y        = vert.y + self.half_cell
            first_point  = Point(x=first_x, y=y)
            second_point = Point(x=second_x, y=y)
        return Line(start=first_point, end=second_point)

    def generate_wall_path_line(self, grid_idx: VCWGridLoc) -> WallPath:
        return WallPath(wall=self.get_line_for_wall(grid_idx),
                        path=self.get_line_for_path(grid_idx))


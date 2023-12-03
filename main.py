from tkinter import Tk, BOTH, Canvas
from typing import Any, Self
import random
from time import sleep
from collections import deque as Deque
from itertools import chain
from dataclasses import dataclass
# import sys

from geometry import Point, Line, Location

from vcw_grid import VCWGrid

@dataclass
class WallPath:
    wall: Line
    path: Line
    solid: bool=True

@dataclass
class Cell:
    point: Point
    visited: bool

class Window():
    def __init__(self, width, height) -> None:
        self.root = Tk()
        self.root.wm_title("Maze Solver")
        self.root.geometry(f"{width}x{height}")
        self.canvas = Canvas(self.root, bg="white", width=width, height=height)
        self.canvas.pack(expand=True, fill=BOTH)
        self.running: bool = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line: Line, fillcolor: str, width: int=2):
        self.canvas.create_line(line.s.x, line.s.y, line.e.x, line.e.y, width=width, fill=fillcolor)

    def draw_point(self, point: Point, fillcolor: str):
        self.canvas.create_rectangle(point.x-3, point.y-3, point.x+3, point.y+3, fill=fillcolor)

upper_corner = Point(5,5)
half_cell_size_x, half_cell_size_y = 15,15
num_rows, num_cols = 20,27
win = Window(820, 610)


def generate_vertical_line_from_midpoint(midpoint: Point):
    return Line(Point(midpoint.x * half_cell_size_x + upper_corner.x,
                      midpoint.y * half_cell_size_y + upper_corner.y - half_cell_size_y),
                Point(midpoint.x * half_cell_size_x + upper_corner.x,
                      midpoint.y * half_cell_size_y + upper_corner.y + half_cell_size_y))

def generate_horizontal_line_from_midpoint(midpoint: Point):
    return Line(Point(midpoint.x * half_cell_size_x + upper_corner.x - half_cell_size_x,
                      midpoint.y * half_cell_size_y + upper_corner.y),
                Point(midpoint.x * half_cell_size_x + upper_corner.x + half_cell_size_x,
                      midpoint.y * half_cell_size_y + upper_corner.y))

def generate_vertical_wall_path_line(row,col):
    # solidity = random.choice([True,False])
    midpoint = Point(col, row)
    return WallPath(wall=generate_vertical_line_from_midpoint(midpoint),
                    path=generate_horizontal_line_from_midpoint(midpoint),
                    solid=True)

def generate_horizontal_wall_path_line(row,col):
    # solidity = random.choice([True,False])
    midpoint = Point(col, row)
    return WallPath(wall=generate_horizontal_line_from_midpoint(midpoint),
                    path=generate_vertical_line_from_midpoint(midpoint),
                    solid=True)


def populate_walls(maze):
    maze.populate_horz_walls(generate_horizontal_wall_path_line)
    maze.populate_vert_walls(generate_vertical_wall_path_line)

def remove_entrance_and_exit() -> None:
    maze_grid.get_north_wall(Location(0, 0)).solid = False
    maze_grid.get_south_wall(Location(num_rows-1, num_cols-1)).solid = False

def draw_walls_and_paths(wall_path: WallPath):
    if not wall_path:
        # print(wall_path)
        return
    if wall_path.solid:
        win.draw_line(wall_path.wall, "black")
    else:
        win.draw_line(wall_path.wall, "white")
    # win.draw_line(wall_path.wall, "black")
    # win.draw_line(wall_path.path, "pink")

def get_unvisited_neighbors(grid: VCWGrid, loc: Location) -> list[Location]:
    def cell_is_not_visited(loc: Location) -> bool:
        return not maze_grid.get_cell(loc).visited
    raw_neighs = maze_grid.get_adjacent_cell_locations(loc)
    result = list(filter(cell_is_not_visited, raw_neighs))
    return result

def remove_wall_with_render(wall: WallPath):
    wall.solid = False
    win.draw_line(wall.wall, "white")

def get_wall_between_cells(from_loc: Location, to_loc: Location):
    delta_row_col = to_loc.row - from_loc.row, to_loc.col - from_loc.col
    # print(delta_row_col)
    match delta_row_col:
        case (-1, 0): # North
            return maze_grid.get_north_wall(from_loc)
        case (1, 0): # South
            return maze_grid.get_south_wall(from_loc)
        case (0, -1): # 
            return maze_grid.get_west_wall(from_loc)
        case (0, 1):
            return maze_grid.get_east_wall(from_loc)

def remove_walls_to_maze():
    start = Location(0, 0)
    path_walked = [start]
    curr_cell = start
    while path_walked:
        maze_grid.get_cell(curr_cell).visited = True
        viable_neighbors = get_unvisited_neighbors(maze_grid, curr_cell)
        if not viable_neighbors:
            curr_cell = path_walked.pop()
            continue
        next_cell = random.choice(viable_neighbors)
        remove_wall_with_render(get_wall_between_cells(curr_cell, next_cell))
        path_walked.append(next_cell)
        curr_cell = next_cell
        win.redraw()

# random.seed(42)
maze_grid = VCWGrid(cell_rows=num_rows, cell_cols=num_cols)
populate_walls(maze_grid)
maze_grid.populate_cells(lambda r,c: Cell(point=None, visited=False))
remove_entrance_and_exit()
maze_grid.map_walls(draw_walls_and_paths)
remove_walls_to_maze()
maze_grid.map_walls(draw_walls_and_paths)
# from pprint import pp
# pp(maze_grid)
# win.draw_line(maze_grid.get_north_wall(Location(4,1)).wall, "green2")
# win.draw_line(maze_grid.get_south_wall(Location(4,1)).wall, "blue")
# win.draw_line(maze_grid.get_east_wall(Location(4,1)).wall, "violet")
# win.draw_line(maze_grid.get_west_wall(Location(4,1)).wall, "gold3")
win.redraw()
win.wait_for_close()

#   __END__
#   # wg = WallGrid(upper_right_corner=Point(25, 25), 
#   #               cell_size_x=50, cell_size_y=50, 
#   #               num_rows=4, num_cols=4)
#   wg = WallGrid(upper_right_corner=Point(0, 0), 
#                 cell_size_x=25, cell_size_y=25, 
#                 num_rows=24, num_cols=32)
#   wg.draw_walls(line_renderer=win.draw_line)
#   # wg.test_draw_center_points(point_renderer=win.draw_point)
#   # wg.test_draw_all_paths(line_renderer=win.draw_line)
#   wg.remove_entrance_and_exit()
#   wg.remove_walls(rerender=win.redraw, line_renderer=win.draw_line)
#   wg.draw_walls(line_renderer=win.draw_line)
#   wg.entry_path.draw(renderer=win.draw_line, color="RoyalBlue2")
#   wg.exit_path.draw(renderer=win.draw_line, color="RoyalBlue2")
#   win.redraw()
#   print("Done removing walls...")



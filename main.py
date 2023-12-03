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
half_cell_size_x, half_cell_size_y = 25,25
num_rows, num_cols = 6,8 


def generate_vertical_line_from_midpoint(midpoint: Point):
    return Line(Point(midpoint.x * half_cell_size_x + upper_corner.x, # half_cell_size_x,
                      midpoint.y * half_cell_size_y + upper_corner.y - half_cell_size_y + 5),
                Point(midpoint.x * half_cell_size_x + upper_corner.x,
                      midpoint.y * half_cell_size_y + upper_corner.y + half_cell_size_y - 5))


def generate_vertical_wall_path_line(row,col):
    def generate_line_pair():
        midpoint = Point(col, row)
        print(f"vert wall(grid_x={row},grid_y={col}) -> midpoint({midpoint.x},{midpoint.y})")
        return (generate_vertical_line_from_midpoint(midpoint),
                generate_horizontal_line_from_midpoint(midpoint))
    wall_line, path_line = generate_line_pair()
    solidity = random.choice([True,False])
    return WallPath(wall=wall_line, path=path_line, solid=solidity)
    pass

def generate_horizontal_line_from_midpoint(midpoint: Point):
    return Line(Point(midpoint.x * half_cell_size_x + upper_corner.x - half_cell_size_x + 5,
                      midpoint.y * half_cell_size_y + upper_corner.y),
                Point(midpoint.x * half_cell_size_x + upper_corner.x + half_cell_size_x - 5,
                      midpoint.y * half_cell_size_y + upper_corner.y))

def generate_horizontal_wall_path_line(row,col):
    def generate_line_pair():
        midpoint = Point(col, row)
        print(f"horz wall(grid_x={row},grid_y={col}) -> midpoint({midpoint.x},{midpoint.y})")
        return (generate_horizontal_line_from_midpoint(midpoint),
                generate_vertical_line_from_midpoint(midpoint))
    wall_line, path_line = generate_line_pair()
    solidity = random.choice([True,False])
    return WallPath(wall=wall_line, path=path_line, solid=solidity)


def populate_walls(maze):
    maze.populate_horz_walls(generate_horizontal_wall_path_line)
    maze.populate_vert_walls(generate_vertical_wall_path_line)


def draw_walls_and_paths(wall_path: WallPath):
    if not wall_path:
        print(wall_path)
        return
    # if wall_path.solid:
    #     win.draw_line(wall_path.wall, "black")
    # else:
    #     win.draw_line(wall_path.path, "pink")
    win.draw_line(wall_path.wall, "black")
    win.draw_line(wall_path.path, "pink")

random.seed(42)
win = Window(810, 610)
maze_grid = VCWGrid(12,16)
populate_walls(maze_grid)
maze_grid.map_walls(draw_walls_and_paths)
# from pprint import pp
# pp(maze_grid)
win.draw_line(maze_grid.get_north_wall(Location(4,1)).wall, "green2")
win.draw_line(maze_grid.get_south_wall(Location(4,1)).wall, "blue")
win.draw_line(maze_grid.get_east_wall(Location(4,1)).wall, "violet")
win.draw_line(maze_grid.get_west_wall(Location(4,1)).wall, "gold3")
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



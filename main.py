from tkinter import Tk, BOTH, Canvas
from typing import Any, Self
import random
from time import sleep
from collections import deque as Deque
from itertools import chain
from dataclasses import dataclass
# import sys
from pprint import pp

from geometry import Point, Line, CellLocation
from vcw_grid import VCWGrid, VCWGridLoc

DEBUG = None

if DEBUG:
    NUM_ROWS     = 6
    NUM_COLS     = 8
    CELL_SIZE    = 85
    BORDER_WIDTH = 25
    random.seed(42)
elif DEBUG is None:
    # silly trick for quick running with no output to logging
    NUM_ROWS     = 8
    NUM_COLS     = 11
    CELL_SIZE    = 35
    BORDER_WIDTH = 25
    random.seed(4177)
else:
    NUM_ROWS     = 20
    NUM_COLS     = 27
    CELL_SIZE    = 35
    BORDER_WIDTH = 5
    seed = random.randint(1, 65536)
    random.seed(seed)
    print("seed=",seed)

@dataclass
class WallPath:
    wall: Line
    path: Line
    solid: bool=True
    path_color: str=None

@dataclass
class Cell:
    loc: CellLocation
    visited: bool

@dataclass
class Vertex:
    point: Point

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
        # print(line)
        self.canvas.create_line(line.start.x, line.start.y, 
                                line.end.x, line.end.y, 
                                width=width, fill=fillcolor)

    def draw_point(self, point: Point, fillcolor: str, width: int=3):
        self.canvas.create_rectangle(point.x-width, point.y-width, 
                                     point.x+width, point.y+width, 
                                     fill=fillcolor)

class GridToScreenTranslator:
    def __init__(self, num_rows: int, num_cols: int,
                 cell_size_in_pixels: int,
                 border_width_in_pixels: int) -> None:
        self.cell_rows = num_rows
        self.cell_cols = num_cols
        self.vertex_rows = num_rows + 1
        self.vertex_cols = num_cols + 1
        if cell_size_in_pixels % 2 == 0: # even sizes have no center pixel
            cell_size_in_pixels += 1
        self.cell_size = cell_size_in_pixels
        self.half_cell = cell_size_in_pixels//2
        self.upper_corner = Point(x=border_width_in_pixels, 
                                  y=border_width_in_pixels)
        screen_width = (2 * border_width_in_pixels
            + num_cols * cell_size_in_pixels)
        screen_height = (2 * border_width_in_pixels
            + num_rows * cell_size_in_pixels)
        self.size = (screen_width, screen_height)
        self.vertex_grid = self.create_vertex_coordinates()
        # pp(self.vertex_grid)

    def create_vertex_coordinates(self):
        # print(self.vertex_rows, self.vertex_cols)
        vertex_grid = []
        for row in range(self.vertex_rows):
            new_row = []
            for col in range(self.vertex_cols):
                x_coord = self.upper_corner.x + col * self.cell_size
                y_coord = self.upper_corner.y + row * self.cell_size
                new_row.append(Point(x=x_coord, y=y_coord))
            vertex_grid.append(new_row)
        return vertex_grid

    def cell_center_point(self, loc: CellLocation) -> Point:
        x_coord = ( self.upper_corner.x
                  + loc.col * self.cell_size
                  + self.half_cell
                  + 1)
        y_coord = ( self.upper_corner.y
                  + loc.row * self.cell_size
                  + self.half_cell
                  + 1)
        return Point(x=x_coord, y=y_coord)

    def get_line_for_wall(self, indexes: VCWGridLoc) -> Line:
        # print("get_line_for_wall indexes are ",indexes)
        if indexes.row % 2 == 0: # horz_wall
            horz_row = indexes.row//2
            horz_start_col = indexes.col//2
            horz_end_col = horz_start_col + 1
            # print(f"horz wall: ({horz_start_col=},{horz_end_col=}), {horz_row=}")
            return Line(start=self.vertex_grid[horz_row][horz_start_col],
                        end=self.vertex_grid[horz_row][horz_end_col])
        else:
            vert_start_row = indexes.row//2
            vert_end_row = vert_start_row + 1
            vert_col = indexes.col//2
            # print("vert wall: ",(vert_start_row,vert_end_row),vert_col)
            return Line(start=self.vertex_grid[vert_start_row][vert_col],
                        end=self.vertex_grid[vert_end_row][vert_col])

    def get_line_for_path(self, indexes: VCWGridLoc) -> Line:
        # print("get_line_for_path indexes are ",indexes)
        vert = self.vertex_grid[indexes.row//2][indexes.col//2]
        # print("vert is ", vert)
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

screen = GridToScreenTranslator(num_rows=NUM_ROWS, num_cols=NUM_COLS,
                                cell_size_in_pixels=CELL_SIZE,
                                border_width_in_pixels=BORDER_WIDTH)
win = Window(*screen.size)

if DEBUG:
    print(screen.vertex_grid)

# def generate_wall_path_line(row,col) -> WallPath:
#     grid_idx = VCWGridLoc(row=row, col=col)
#     return WallPath(wall=screen.get_line_for_wall(grid_idx),
#                     path=screen.get_line_for_path(grid_idx))
#
# def populate_walls(maze: VCWGrid) -> None:
#     maze.populate_horz_walls(generate_wall_path_line)
#     maze.populate_vert_walls(generate_wall_path_line)

def remove_entrance_and_exit(maze: VCWGrid) -> None:
    maze.get_north_wall(CellLocation(row=0, col=0)).solid = False
    maze.get_south_wall(CellLocation(row=screen.cell_rows-1, col=screen.cell_cols-1)).solid = False

def draw_walls_and_paths(wall_path: WallPath):
    if not wall_path:
        # print(wall_path)
        return
    if wall_path.solid:
        win.draw_line(wall_path.wall, "black")
    else:
        if color := wall_path.path_color:
            win.draw_line(wall_path.path, color)
    # win.draw_line(wall_path.wall, "black")
    # win.draw_line(wall_path.path, "pink")

def get_unvisited_neighbors(grid: VCWGrid, loc: CellLocation) -> list[CellLocation]:
    def cell_is_not_visited(loc: CellLocation) -> bool:
        return not maze_grid.get_cell(loc).visited
    raw_neighs = maze_grid.get_adjacent_cell_locations(loc)
    result = list(filter(cell_is_not_visited, raw_neighs))
    return result

def remove_wall_with_render(wall: WallPath):
    wall.solid = False
    win.draw_line(wall.wall, "white")

def get_wallpath_between_cell_locations(from_loc: CellLocation, 
                                        to_loc: CellLocation) -> WallPath:
    delta_row_col = to_loc.row - from_loc.row, to_loc.col - from_loc.col
    # print(delta_row_col)
    match delta_row_col:
        case (-1, 0): # North
            if DEBUG:
                print(f"North")
            return maze_grid.get_north_wall(from_loc)
        case (1, 0): # South
            if DEBUG:
                print(f"South")
            return maze_grid.get_south_wall(from_loc)
        case (0, -1): # 
            if DEBUG:
                print(f"West")
            return maze_grid.get_west_wall(from_loc)
        case (0, 1):
            if DEBUG:
                print(f"East")
            return maze_grid.get_east_wall(from_loc)

def remove_walls_to_maze():
    start = CellLocation(row=screen.cell_rows-1, col=screen.cell_cols-1)
    path_walked = [start]
    curr_cell = start
    while True:
        maze_grid.get_cell(curr_cell).visited = True
        viable_neighbors = get_unvisited_neighbors(maze_grid, curr_cell)
        if viable_neighbors:
            if DEBUG:
                print(f"{viable_neighbors=}")
            next_cell = random.choice(viable_neighbors)
            if DEBUG:
                print(f"{next_cell=}")
            between = get_wallpath_between_cell_locations(curr_cell, next_cell)
            if DEBUG:
                print(f"{between=}")
            
            remove_wall_with_render(between)
            path_walked.append(next_cell)
            curr_cell = next_cell
        else:
            path_walked.pop()            
            if not path_walked:   # empty path means we are done
                break
            curr_cell = path_walked[-1]
        win.redraw()

# def get_reachable_unvisited_neighbors(loc: CellLocation) -> list[CellLocation]:
#     def path_exists_between(neigh):
#         between: WallPath = get_wallpath_between_cell_locations(loc, neigh)
#         wall_between_is_solid = between.solid
#         return not wall_between_is_solid
#     unvisited = get_unvisited_neighbors(maze_grid, loc)
#     return list(filter(path_exists_between, unvisited))
#
# def color_backtrack_path_backtrack_color(from_loc: CellLocation, 
#                                          to_loc: CellLocation) -> None:
#     backtrack_color = "goldenrod2"
#     wall_between = get_wallpath_between_cell_locations(from_loc, to_loc)
#     wall_between.path_color = backtrack_color
#     win.draw_line(wall_between.path, backtrack_color)
#
# def color_forward_path_forward_pass_color(from_loc: CellLocation, 
#                                           to_loc: CellLocation) -> None:
#     forward_pass_color = "blue"
#     # print(f"{from_loc=}\t{to_loc=}")
#     wall_between = get_wallpath_between_cell_locations(from_loc, to_loc)
#     wall_between.path_color = forward_pass_color
#     win.draw_line(wall_between.path, forward_pass_color)

def mark_cell_unvisited(cell: Cell) -> None:
    cell.visited = False

def run_maze() -> bool:
    def get_reachable_unvisited_neighbors(loc: CellLocation) -> list[CellLocation]:
        def path_exists_between(neigh):
            between: WallPath = get_wallpath_between_cell_locations(loc, neigh)
            wall_between_is_solid = between.solid
            return not wall_between_is_solid
        unvisited = get_unvisited_neighbors(maze_grid, loc)
        return list(filter(path_exists_between, unvisited))

    def color_backtrack_path_backtrack_color(from_loc: CellLocation, 
                                             to_loc: CellLocation) -> None:
        backtrack_color = "goldenrod2"
        wall_between = get_wallpath_between_cell_locations(from_loc, to_loc)
        wall_between.path_color = backtrack_color
        win.draw_line(wall_between.path, backtrack_color)

    def color_forward_path_forward_pass_color(from_loc: CellLocation, 
                                              to_loc: CellLocation) -> None:
        forward_pass_color = "blue"
        # print(f"{from_loc=}\t{to_loc=}")
        wall_between = get_wallpath_between_cell_locations(from_loc, to_loc)
        wall_between.path_color = forward_pass_color
        win.draw_line(wall_between.path, forward_pass_color)

    start = CellLocation(row=0, col=0)
    destination_cell = CellLocation(row=screen.cell_rows-1, 
                                    col=screen.cell_cols-1)
    path_walked = [start]
    curr_cell = start
    while True:
        sleep(0.1)
        maze_grid.get_cell(curr_cell).visited = True
        viable_neighbors = get_reachable_unvisited_neighbors(curr_cell)
        if curr_cell == destination_cell:
            # print("Maze solved")
            return True
        if viable_neighbors:
            next_cell = random.choice(viable_neighbors)
            color_forward_path_forward_pass_color(curr_cell, next_cell)
            path_walked.append(next_cell)
            curr_cell = next_cell
        else:
            prev_cell = path_walked.pop()
            if not path_walked:
                # print("Maze is not solvable")
                return False
            curr_cell = path_walked[-1]
            color_backtrack_path_backtrack_color(prev_cell, curr_cell)
        win.redraw()

def draw_start_location_dot():
    width = screen.half_cell//2
    start_coord = screen.cell_center_point(CellLocation(row=0,col=0))
    win.draw_point(start_coord, "blue", width=width)

def draw_end_location_dot():
    width = screen.half_cell//2
    end_coord = screen.cell_center_point(CellLocation(row=screen.cell_rows-1,
                                                      col=screen.cell_cols-1))
    win.draw_point(end_coord, "blue", width=width)

maze_grid = VCWGrid(cell_rows=screen.cell_rows, cell_cols=screen.cell_cols)
if DEBUG:
    print("------------------------------------------ start -")
    pp(maze_grid._grid)
    print("------------------------------------------ end ---")
maze_grid.populate_walls(screen.generate_wall_path_line)
# populate_walls(maze_grid)
if DEBUG:
    print("------------------------------------------ start -")
    print(maze_grid._grid)
    print("------------------------------------------ end ---")
for cell_loc in maze_grid.cells_locs():
    maze_grid.set_cell(cell_loc, Cell(loc=cell_loc, visited=False))
draw_start_location_dot()
remove_entrance_and_exit(maze_grid)
maze_grid.map_walls(draw_walls_and_paths)
remove_walls_to_maze()
maze_grid.map_walls(draw_walls_and_paths)
maze_grid.map_cells(mark_cell_unvisited)
if DEBUG:
    pp(maze_grid._grid)
    win.draw_line(maze_grid.get_north_wall(CellLocation(row=2, col=1)).wall, "green2")
    win.draw_line(maze_grid.get_south_wall(CellLocation(row=2, col=1)).wall, "blue")
    win.draw_line(maze_grid.get_east_wall(CellLocation(row=2, col=1)).wall, "violet")
    win.draw_line(maze_grid.get_west_wall(CellLocation(row=2, col=1)).wall, "gold3")
win.redraw()
sleep(0.5)
draw_start_location_dot()
if run_maze():
    draw_end_location_dot()
win.wait_for_close()


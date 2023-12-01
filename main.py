from tkinter import Tk, BOTH, Canvas
from typing import Any, Self
import random
from time import sleep
from collections import deque as Deque
from itertools import chain

from geometry import Point, Line

import sys

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

from wall import Wall, WallGrid

def main():
    random.seed(42)
    win = Window(800, 600)
    wg = WallGrid(upper_right_corner=Point(25, 25), 
                  cell_size_x=50, cell_size_y=50, 
                  num_rows=11, num_cols=15)
    wg.draw_walls(line_renderer=win.draw_line)
    # wg.test_draw_center_points(point_renderer=win.draw_point)
    # wg.test_draw_all_paths(line_renderer=win.draw_line)
    win.redraw()
    wg.remove_entrance_and_exit()
    wg.draw_walls(line_renderer=win.draw_line)
    wg.remove_walls(temp=win.redraw, line_renderer=win.draw_line)
    print("Done removing walls...")
    wg.entry_path.draw(renderer=win.draw_line, color="RoyalBlue2")
    wg.exit_path.draw(renderer=win.draw_line, color="RoyalBlue2")
    win.redraw()
    win.wait_for_close()

if __name__ == "__main__":
    main()


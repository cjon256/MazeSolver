from tkinter import Tk, BOTH, Canvas
from typing import Any, Self
import random
from time import sleep
from collections import deque as Deque
from itertools import chain

from shapes import Point, Line

import sys

def close(event):
    sys.exit() # if you want to exit the entire thing

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

    def draw_line(self, line: Line, fillcolor: str):
        line.draw(self.canvas, fillcolor)

    # def draw_cell(self, cell: Cell, fillcolor: str):
    #     cell.draw(self.canvas, fillcolor)
    #
    # def draw_line_between_cells(self, from_cell: Cell, to_cell: Cell) -> None:
    #     from_cell.draw_move(self.canvas, to_cell)

from wall import Wall, WallGrid


def main():
    random.seed(42)
    win = Window(800, 600)
    #    mz = Maze(upper_right_corner=Point(25, 25), 
    #              num_rows=11, num_cols=15, 
    #              cell_size_x=50, cell_size_y=50, 
    #              win=win)
    #    mz._break_entrance_and_exit()
    #    # mz._draw_all_cells()
    #    mz._break_walls_r(2,2)
    #    mz._animate()
    wg = WallGrid(upper_right_corner=Point(25, 25), 
                  cell_size_x=50, cell_size_y=50, 
                  num_rows=3, num_cols=2)
    wg.lr_walls[0][0].solid = False
    wg.draw_walls(line_renderer=win.draw_line)

    win.wait_for_close()


if __name__ == "__main__":
    main()


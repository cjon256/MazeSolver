from tkinter import Tk, BOTH, Canvas
from typing import Any, Self
import random
from time import sleep
from collections import deque as Deque

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point(x={self.x}, y={self.y})"

class Line:
    def __init__(self, start: Point, end: Point) -> None:
        self.s, self.e = start, end

    def draw(self, canvas: Canvas, fillcolor: str):
        canvas.create_line(self.s.x, self.s.y, self.e.x, self.e.y, fill=fillcolor)

class Cell:
    def __init__(self,
                 has_left_wall: bool,
                 has_right_wall: bool,
                 has_top_wall: bool,
                 has_bottom_wall: bool,
                 up_left: Point,
                 down_right: Point) -> None:
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        up_right = Point(down_right.x, up_left.y)
        down_left = Point(up_left.x, down_right.y)
        self.top_line = Line(up_left, up_right)
        self.right_line = Line(up_right, down_right)
        self.left_line = Line(up_left, down_left)
        self.bottom_line = Line(down_left, down_right)
        self.center_point = Point((up_left.x + down_right.x)//2,
                                  (up_left.y + down_right.y)//2)
        self.visited = False

    def __str__(self):
        return f"Cell(has_lines={[self.has_left_wall, self.has_right_wall, self.has_top_wall, self.has_bottom_wall]})"

    def draw(self, canvas: Canvas, fillcolor: str) -> None:
        if self.has_top_wall:
            self.top_line.draw(canvas, fillcolor)
        else:
            self.top_line.draw(canvas, "white")
        if self.has_bottom_wall:
            self.bottom_line.draw(canvas, fillcolor)
        else:
            self.bottom_line.draw(canvas, "white")
        if self.has_left_wall:
            self.left_line.draw(canvas, fillcolor)
        else:
            self.left_line.draw(canvas, "white")
        if self.has_right_wall:
            self.right_line.draw(canvas, fillcolor)
        else:
            self.right_line.draw(canvas, "white")

    def draw_move(self, canvas: Canvas, to_cell: Self, undo: bool=False) -> None:
        new_line = Line(self.center_point, to_cell.center_point)
        fillcolor = "gray" if undo else "red"
        new_line.draw(canvas, fillcolor)

    def get_walls(self: Self) -> tuple[bool,bool,bool,bool]:
        return (self.has_left_wall,
                self.has_right_wall,
                self.has_top_wall,
                self.has_bottom_wall)

    def number_of_walls(self: Self) -> int:
        return sum([1 for w in self.get_walls() if w == True])


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

    def draw_cell(self, cell: Cell, fillcolor: str):
        cell.draw(self.canvas, fillcolor)

    def draw_line_between_cells(self, from_cell: Cell, to_cell: Cell) -> None:
        from_cell.draw_move(self.canvas, to_cell)

class CellGrid:
    def __init__(self,
                 num_rows: int,
                 num_cols: int,
                 ):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cells = self.create_cell_grid()

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

class Maze:
    def __init__(self,
                 upper_right_corner: Point,
                 num_rows: int,
                 num_cols: int,
                 cell_size_x: int,
                 cell_size_y: int,
                 win: Window = None) -> None:
        """
        Initializes data members for all its inputs, then calls its _create_cells() method
        """
        self.x1 = upper_right_corner.x
        self.y1 = upper_right_corner.y
        self.urc = upper_right_corner
        self.dims = { 'rows': num_rows, 'cols': num_cols }
        self.cell_size = Point(cell_size_x, cell_size_y)
        self.win = win
        self.cells = self._create_cells()

    def _create_cells(self) -> None:
        """
        _CREATE_CELLS()
        This method should fill a self._cells list with lists of cells. Each top-level list is a column of
        Cell objects. Once matrix is populated it should call its _draw_cell() method on each Cell.
        """
        all_cells: list[Cell] = []
        for row_number in range(self.dims["rows"]):
            row = []
            for col_number in range(self.dims["cols"]):
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

    def _draw_all_cells(self) -> None:
        fillcolor = "black"
        for row in self.cells:
            for cell in row:
                self.win.draw_cell(cell, fillcolor)

    def _draw_cell(self: Self, i: int, j: int) -> None:
        """
        _DRAW_CELL(SELF, I, J) 
        This method should calculate the x/y position of the Cell based on i, j, the cell_size, and the x/y
        position of the Maze itself. The x/y position of the maze represents how many pixels from the top and
        left the maze should start from the side of the window. Once that's calculated, it should draw the
        cell and call the maze's _animate() method.
        """
        cell = self.cells[i][j]
        fillcolor = "black"
        self.win.draw_cell(cell, fillcolor)

    def _animate(self: Self) -> None:
        """
        _ANIMATE(SELF)
        The animate method is what allows us to visualize what the algorithms are doing in real time. It
        should simply call the window's redraw() method, then sleep for a short amount of time so your eyes
        keep up with each render frame. I slept for 0.05 seconds.
        """
        self.win.redraw()
        sleep(0.05)

    def _break_entrance_and_exit(self) -> None:
        """
        _break_entrance_and_exit() - The entrance to the maze will always be at the top of the top-left cell,
        the exit always at the bottom of the bottom-right cell.
        """
        self.cells[0][0].has_top_wall = False
        self.cells[self.dims["rows"] - 1][self.dims["cols"] - 1].has_bottom_wall = False
        self._draw_all_cells()

    def _break_walls_r(self, i: int, j: int) -> None:
        """ 
        _BREAK_WALLS_R(SELF, I, J)
        The recursive break_walls_r method is a depth-first traversal through the cells, breaking down walls
        as it goes. I'll describe the algorithm I used, but feel free to write your own from scratch if you're
        up to it!

        1. Mark the current cell as visited 
        2. In an infinite loop: 
           1. Create a new empty list to hold the i and j values you will need to visit 
           2. Check the cells that are directly adjacent to the current cell. Keep track of any that have not
              been visited as "possible directions" to move to 
           3. If there are zero directions you can go from the current cell, then draw the current cell and
              return to break out of the loop 
           4. Otherwise, pick a random direction. 
           5. Knock down the walls between the current cell and the chosen cell. 
           6. Move to the chosen cell by recursively calling _break_walls_r
        """

        def get_leftward_cell(row: int, col: int) -> Cell:
            return self.cells[row][col-1]

        def get_rightward_cell(row: int, col: int) -> Cell:
            return self.cells[row][col+1]

        def get_upward_cell(row: int, col: int) -> Cell:
            return self.cells[row-1][col]

        def get_downward_cell(row: int, col: int) -> Cell:
            return self.cells[row+1][col]

        def find_unvisited_cell_neighbors(row: int, col: int) -> list[Cell]:
            print(row,col,self.dims["cols"])
            neigh = []
            if is_not_final_column(col):
                right_cell = self.cells[row][col+1]
                if not right_cell.visited:
                    right_cell.visited = True
                    neigh.append((row,col+1))
            return neigh

        def break_wall_left(row: int, col: int) -> None:
            self.cells[row][col].has_left_wall = False
            get_leftward_cell(row, col).has_right_wall = False

        def break_wall_right(row: int, col: int) -> None:
            self.cells[row][col].has_right_wall = False
            get_rightward_cell(row, col).has_left_wall = False

        def break_wall_top(row: int, col: int) -> None:
            self.cells[row][col].has_top_wall = False
            get_upward_cell(row, col).has_bottom_wall = False

        def break_wall_bottom(row: int, col: int) -> None:
            self.cells[row][col].has_bottom_wall = False
            get_downward_cell(row, col).has_top_wall = False

        def is_not_final_column(col: int) -> bool:
            return col < self.dims["cols"] - 1 

        def is_not_first_column(col: int) -> bool:
            return col > 0

        def is_not_final_row(row: int) -> bool:
            return row < self.dims["rows"] - 1 

        def is_not_first_row(row: int) -> bool:
            return row > 0

        to_visit = Deque()
        path = []
        print(i,j)
        to_visit.append((i,j))
        while to_visit:
            row, col = to_visit.popleft()
            print(f"visiting: {row},{col}")
            adj = find_unvisited_cell_neighbors(row, col)
            for node in adj:
                to_visit.append(node)
            if is_not_final_column(col):
                break_wall_right(row, col)
        self._draw_all_cells()

# win.draw_line(Line(Point(100, 100), Point(350, 300)), "Red")
# l = Line(Point(50, 50), Point(400, 400))
# win.draw_line(l, "black")
# c1 = Cell(has_left_wall=False, has_right_wall=True,
#          has_top_wall=True, has_bottom_wall=True,
#          up_left=Point(500,500), down_right=Point(550, 550))
# win.draw_cell(c1, "green")
# c2 = Cell(has_left_wall=False, has_right_wall=False,
#          has_top_wall=True, has_bottom_wall=True,
#          up_left=Point(450,500), down_right=Point(500, 550))
# win.draw_cell(c2, "green")
# win.draw_line_between_cells(c1, c2)

def main():
    random.seed(42)
    win = Window(800, 600)
    mz = Maze(upper_right_corner=Point(25, 25), 
              num_rows=11, num_cols=15, 
              cell_size_x=50, cell_size_y=50, 
              win=win)
    mz._break_entrance_and_exit()
    # mz._draw_all_cells()
    mz._break_walls_r(2,2)
    mz._animate()

    win.wait_for_close()


if __name__ == "__main__":
    main()


from tkinter import Tk, BOTH, Canvas

from geometry import Point, Line 

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
        self.canvas.create_line(line.start.x, line.start.y, 
                                line.end.x, line.end.y, 
                                width=width, fill=fillcolor)

    def draw_point(self, point: Point, fillcolor: str, width: int=3):
        self.canvas.create_rectangle(point.x-width, point.y-width, 
                                     point.x+width, point.y+width, 
                                     fill=fillcolor)


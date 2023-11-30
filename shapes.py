from tkinter import Tk, BOTH, Canvas
from typing import Any, Self

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

class Line:
    def __init__(self: Self, start: Point, end: Point) -> None:
        self.s, self.e = start, end

    def draw(self: Self, canvas: Canvas, fillcolor: str):
        canvas.create_line(self.s.x, self.s.y, self.e.x, self.e.y, fill=fillcolor)

    def __repr__(self: Self):
        return f"Line(start={self.s}, end={self.e})"


from tkinter import Tk, BOTH, Canvas
from typing import Any, Self
from dataclasses import dataclass

@dataclass(kw_only=True, frozen=True)
class Point:
    x: int 
    y: int

@dataclass(kw_only=True, frozen=True)
class Line:
    start: Point
    end: Point

@dataclass(kw_only=True, frozen=True)
class CellLocation:
    row: int
    col: int


from tkinter import Tk, BOTH, Canvas
from typing import Any, Self
from dataclasses import dataclass

@dataclass
class Point:
    x: int 
    y: int

@dataclass
class Line:
    s: Point
    e: Point

@dataclass
class Location:
    row: int
    col: int


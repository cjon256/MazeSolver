from dataclasses import dataclass

from geometry import Point, Line, CellLocation

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

@dataclass(frozen=True)
class Vertex:
    point: Point


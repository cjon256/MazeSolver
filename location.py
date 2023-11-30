from typing import Self

class Location:
    def __init__(self: Self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    def __str__(self: Self):
        return f"Location(row={self.row}, col={self.col})"


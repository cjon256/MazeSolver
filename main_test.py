import unittest

from main import Maze, Point

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(upper_right_corner=Point(0, 0), num_rows=num_rows, num_cols=num_cols, cell_size_x=10, cell_size_y=10)
        print(len(m1.cells),len(m1.cells[0]))
        self.assertEqual(
            len(m1.cells),
            num_rows
        )
        self.assertEqual(
            len(m1.cells[0]),
            num_cols
        )

if __name__ == "__main__":
    unittest.main()

import unittest
import itertools
from pprint import pp

from geometry import Location
from vcw_grid import VCWGrid

class Tests(unittest.TestCase):
    def test_vcw_grid_stucture(self):
        arr2x3 = [[None, None, None, None, None, None, None],
                  [None, None, None, None, None, None, None],
                  [None, None, None, None, None, None, None],
                  [None, None, None, None, None, None, None],
                  [None, None, None, None, None, None, None]]

        grid2x3 = VCWGrid(2, 3)
        self.assertEqual(
            arr2x3,
            grid2x3._grid
        )

    def test_vcw_grid_cell_iter(self):
        arr2x3 = [['v', 'w', 'v', 'w', 'v', 'w', 'v'],
                  ['w', 'c', 'w', 'c', 'w', 'c', 'w'],
                  ['v', 'w', 'v', 'w', 'v', 'w', 'v'],
                  ['w', 'c', 'w', 'c', 'w', 'c', 'w'],
                  ['v', 'w', 'v', 'w', 'v', 'w', 'v']]

        grid2x3 = VCWGrid(2, 3)
        grid2x3._grid = arr2x3
        all_v_predicted = list(filter(lambda s: s == 'c', itertools.chain(*arr2x3)))
        all_v_result = [ *grid2x3.cells() ]

        self.assertEqual(
            all_v_predicted,
            all_v_result
        )

    def test_vcw_grid_wall_iter(self):
        arr2x3 = [['v', 'w', 'v', 'w', 'v', 'w', 'v'],
                  ['w', 'c', 'w', 'c', 'w', 'c', 'w'],
                  ['v', 'w', 'v', 'w', 'v', 'w', 'v'],
                  ['w', 'c', 'w', 'c', 'w', 'c', 'w'],
                  ['v', 'w', 'v', 'w', 'v', 'w', 'v']]

        grid2x3 = VCWGrid(2, 3)
        grid2x3._grid = arr2x3
        all_v_predicted = list(filter(lambda s: s == 'w', itertools.chain(*arr2x3)))
        all_v_result = [ *grid2x3.walls() ]

        self.assertEqual(
            all_v_predicted,
            all_v_result
        )

    def test_vcw_grid_vertex_iter(self):
        arr2x3 = [['v', 'w', 'v', 'w', 'v', 'w', 'v'],
                  ['w', 'c', 'w', 'c', 'w', 'c', 'w'],
                  ['v', 'w', 'v', 'w', 'v', 'w', 'v'],
                  ['w', 'c', 'w', 'c', 'w', 'c', 'w'],
                  ['v', 'w', 'v', 'w', 'v', 'w', 'v']]
 
        grid2x3 = VCWGrid(2, 3)
        grid2x3._grid = arr2x3
        all_v_predicted = list(filter(lambda s: s == 'v', itertools.chain(*arr2x3)))
        all_v_result = [ *grid2x3.vertexes() ]
 
        self.assertEqual(
            all_v_predicted,
            all_v_result
        )

    def test_vcw_apply_to_vertexes(self):
        arr2x3 = [['v', None, 'v', None, 'v', None, 'v'],
                  [None, None, None, None, None, None, None],
                  ['v', None, 'v', None, 'v', None, 'v'],
                  [None, None, None, None, None, None, None],
                  ['v', None, 'v', None, 'v', None, 'v']]

        grid2x3 = VCWGrid(2, 3)
        grid2x3.apply_to_vertexes(lambda _: 'v')
        self.assertEqual(
            arr2x3,
            grid2x3._grid
        )


    def test_vcw_apply_to_cells(self):
        arr2x3 = [[None, None, None, None, None, None, None],
                  [None, 'c', None, 'c', None, 'c', None],
                  [None, None, None, None, None, None, None],
                  [None, 'c', None, 'c', None, 'c', None],
                  [None, None, None, None, None, None, None]]

        grid2x3 = VCWGrid(2, 3)
        grid2x3.apply_to_cells(lambda _: 'c')
        self.assertEqual(
            arr2x3,
            grid2x3._grid
        )

    def test_vcw_populate_horz_walls(self):
        arr2x3 = [[None, 'w', None, 'w', None, 'w', None],
                  [None, None, None, None, None, None, None],
                  [None, 'w', None, 'w', None, 'w', None],
                  [None, None, None, None, None, None, None],
                  [None, 'w', None, 'w', None, 'w', None]]

        grid2x3 = VCWGrid(2, 3)
        grid2x3.populate_horz_walls(lambda r,c: 'w')
        self.assertEqual(
            arr2x3,
            grid2x3._grid
        )

    def test_vcw_populate_vert_walls(self):
        arr2x3 = [[None, None, None, None, None, None, None],
                  ['w', None, 'w', None, 'w', None, 'w'],
                  [None, None, None, None, None, None, None],
                  ['w', None, 'w', None, 'w', None, 'w'],
                  [None, None, None, None, None, None, None]]

        grid2x3 = VCWGrid(2, 3)
        grid2x3.populate_vert_walls(lambda r,c: 'w')
        self.assertEqual(
            arr2x3,
            grid2x3._grid
        )

    # def test_vcw_map_walls(self):
    #     arr2x3 = [[None, 'w', None, 'w', None, 'w', None],
    #               ['w', None, 'w', None, 'w', None, 'w'],
    #               [None, 'w', None, 'w', None, 'w', None],
    #               ['w', None, 'w', None, 'w', None, 'w'],
    #               [None, 'w', None, 'w', None, 'w', None]]
    #
    #     grid2x3 = VCWGrid(2, 3)
    #     grid2x3.map_walls(lambda: 'w')
    #     self.assertEqual(
    #         arr2x3,
    #         grid2x3._grid
    #     )

    def test_vcw_grid_get_cell(self):
        arr2x3 = [['v', 'w', 'v', 'w', 'v', 'w', 'v'],
                  ['w', 'c0-0', 'w', 'c0-1', 'w', 'c0-2', 'w'],
                  ['v', 'w', 'v', 'w', 'v', 'w', 'v'],
                  ['w', 'c1-0', 'w', 'c1-1', 'w', 'c1-2', 'w'],
                  ['v', 'w', 'v', 'w', 'v', 'w', 'v']]

        grid2x3 = VCWGrid(2, 3)
        grid2x3._grid = arr2x3
        cell_result = grid2x3.get_cell(Location(1, 1))


        self.assertEqual(
            cell_result, 
            'c1-1' )

    def test_vcw_grid_get_walls(self):
        arr2x3 = [['v', 'w', 'v', 'w', 'v', 'w', 'v'],
                  ['w', 'c', 'w', 'c', 'w4', 'c', 'w'],
                  ['v', 'w1', 'v', 'w2', 'v', 'w', 'v'],
                  ['w', 'c', 'w', 'c', 'w3', 'c', 'w'],
                  ['v', 'w', 'v', 'w', 'v', 'w', 'v']]

        grid2x3 = VCWGrid(2, 3)
        grid2x3._grid = arr2x3
        four_walls_predicted = [ 'w1', 'w2', 'w3', 'w4' ]
        four_walls_result_1 = [ 
            grid2x3.get_north_wall(Location(1, 0)),
            grid2x3.get_south_wall(Location(0, 1)),
            grid2x3.get_east_wall(Location(1, 1)),
            grid2x3.get_west_wall(Location(0, 2)),
        ]
        self.assertEqual(
            four_walls_predicted,
            four_walls_result_1
        )
        four_walls_result_2 = [ 
            grid2x3.get_south_wall(Location(0, 0)),
            grid2x3.get_north_wall(Location(1, 1)),
            grid2x3.get_west_wall(Location(1, 2)),
            grid2x3.get_east_wall(Location(0, 1)),
        ]
        self.assertEqual(
            four_walls_predicted,
            four_walls_result_2
        )

    def test_vcw_grid_get_adjacent_cells(self):
        arr3x3 = [['v', 'w', 'v', 'w', 'v', 'w', 'v'],
                  ['w', 'c', 'w', 'c1', 'w', 'c', 'w'],
                  ['v', 'w', 'v', 'w', 'v', 'w', 'v'],
                  ['w', 'c4', 'w', 'c', 'w', 'c3', 'w'],
                  ['v', 'w', 'v', 'w', 'v', 'w', 'v'],
                  ['w', 'c', 'w', 'c2', 'w', 'c', 'w'],
                  ['v', 'w', 'v', 'w', 'v', 'w', 'v']]

        grid3x3 = VCWGrid(3, 3)
        grid3x3._grid = arr3x3
        four_cells_predicted = [ 'c1', 'c2', 'c3', 'c4' ]
        four_cells_result = grid3x3.get_adjacent_cells(Location(1, 1))
        self.assertEqual(
            four_cells_predicted,
            four_cells_result
        )
        two_cells_predicted = [ 'c4', 'c1' ]
        two_cells_result = grid3x3.get_adjacent_cells(Location(0,0))
        self.assertEqual(
            two_cells_predicted,
            two_cells_result
        )



if __name__ == "__main__":
    unittest.main()

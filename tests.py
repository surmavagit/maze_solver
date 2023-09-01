import unittest
from maze_solver import Maze
import random

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
                len(m1._cells),
                num_cols
                )
        self.assertEqual(
                len(m1._cells[0]),
                num_rows
                )
    def test_maze_break_entrance_exit(self):
        num_cols = 23
        num_rows = 6
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._break_entrance_and_exit()
        self.assertEqual(
                m1._cells[0][0].has_north_wall,
                False
                )
        index_last_col = len(m1._cells) - 1
        index_last_cell = len(m1._cells[index_last_col]) - 1
        self.assertEqual(
                m1._cells[index_last_col ][index_last_cell].has_south_wall,
                False
                )
    def test_maze_reset_visited(self):
        num_cols = 23
        num_rows = 6
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._break_walls_r(0, 0)
        m1._reset_cells_visited()
        self.assertEqual(
            m1._cells[random.randrange(0, num_cols)][random.randrange(0, num_rows)].visited,
            False
        )
                

if __name__ == "__main__":
    unittest.main()

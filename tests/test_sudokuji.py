import unittest

from solver import parse_grid, solve_all
from strategies import mrv


class SudokuSolverTests(unittest.TestCase):
    def test_one_solution(self):
        grid = parse_grid(
            "530070000"
            "600195000"
            "098000060"
            "800060003"
            "400803001"
            "700020006"
            "060000280"
            "000419005"
            "000080079"
        )
        solutions, _ = solve_all(grid, mrv, max_solutions=2)
        self.assertEqual(len(solutions), 1)

    def test_no_solution(self):
        grid = parse_grid(
            "550070000"
            "600195000"
            "098000060"
            "800060003"
            "400803001"
            "700020006"
            "060000280"
            "000419005"
            "000080079"
        )
        solutions, _ = solve_all(grid, mrv, max_solutions=2)
        self.assertEqual(len(solutions), 0)

    def test_multiple_solutions(self):
        grid = parse_grid(
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
            "000000000"
        )
        solutions, _ = solve_all(grid, mrv, max_solutions=2)
        self.assertEqual(len(solutions), 2)


if __name__ == "__main__":
    unittest.main()

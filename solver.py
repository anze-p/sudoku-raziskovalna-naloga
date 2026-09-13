from copy import deepcopy
from dataclasses import dataclass
from typing import Callable, Optional

Grid = list[list[int]]
Selector = Callable[[Grid], Optional[tuple[int, int]]]


@dataclass
class SolveStats:
    attempts: int = 0
    recursive_calls: int = 0
    backtracks: int = 0
    solutions: int = 0


def is_valid_initial_grid(grid: Grid) -> bool:
    """Preveri, ali začetna postavitev že vsebuje kršitev pravil sudokuja."""
    if len(grid) != 9 or any(len(row) != 9 for row in grid):
        return False

    for row in grid:
        if any(value < 0 or value > 9 for value in row):
            return False

    for r in range(9):
        for c in range(9):
            value = grid[r][c]
            if value == 0:
                continue
            grid[r][c] = 0
            ok = is_allowed(grid, r, c, value)
            grid[r][c] = value
            if not ok:
                return False
    return True


def is_allowed(grid: Grid, row: int, col: int, value: int) -> bool:
    if any(grid[row][c] == value for c in range(9)):
        return False
    if any(grid[r][col] == value for r in range(9)):
        return False

    br = (row // 3) * 3
    bc = (col // 3) * 3
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            if grid[r][c] == value:
                return False
    return True


def candidates(grid: Grid, row: int, col: int) -> list[int]:
    if grid[row][col] != 0:
        return []
    return [value for value in range(1, 10) if is_allowed(grid, row, col, value)]


def solve_all(
    grid: Grid,
    selector: Selector,
    max_solutions: int | None = None,
) -> tuple[list[Grid], SolveStats]:
    """Poišče vse rešitve oziroma največ max_solutions rešitev."""
    if not is_valid_initial_grid(grid):
        return [], SolveStats()

    work = deepcopy(grid)
    solutions: list[Grid] = []
    stats = SolveStats()

    def backtrack() -> bool:
        stats.recursive_calls += 1

        position = selector(work)
        if position is None:
            solutions.append(deepcopy(work))
            stats.solutions += 1
            return max_solutions is not None and len(solutions) >= max_solutions

        row, col = position
        possible = candidates(work, row, col)

        for value in possible:
            stats.attempts += 1
            work[row][col] = value
            should_stop = backtrack()
            work[row][col] = 0

            if should_stop:
                return True

        stats.backtracks += 1
        return False

    backtrack()
    return solutions, stats


def solve_first(grid: Grid, selector: Selector) -> tuple[Grid | None, SolveStats]:
    solutions, stats = solve_all(grid, selector, max_solutions=1)
    return (solutions[0] if solutions else None), stats


def parse_grid(text: str) -> Grid:
    chars = [ch for ch in text if ch.isdigit() or ch == "."]
    if len(chars) != 81:
        raise ValueError("Sudoku mora vsebovati natanko 81 polj.")
    values = [0 if ch in {"0", "."} else int(ch) for ch in chars]
    return [values[i : i + 9] for i in range(0, 81, 9)]


def grid_to_string(grid: Grid) -> str:
    return "".join(str(value) for row in grid for value in row)

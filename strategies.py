from typing import Optional
from solver import Grid, candidates


def first_empty_by_rows(grid: Grid) -> Optional[tuple[int, int]]:
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return r, c
    return None


def first_empty_by_columns(grid: Grid) -> Optional[tuple[int, int]]:
    for c in range(9):
        for r in range(9):
            if grid[r][c] == 0:
                return r, c
    return None


def mrv(grid: Grid) -> Optional[tuple[int, int]]:
    best = None
    best_count = 10

    for r in range(9):
        for c in range(9):
            if grid[r][c] != 0:
                continue
            count = len(candidates(grid, r, c))
            if count < best_count:
                best = (r, c)
                best_count = count
                if count <= 1:
                    return best
    return best


STRATEGIES = {
    "rows": first_empty_by_rows,
    "columns": first_empty_by_columns,
    "mrv": mrv,
}

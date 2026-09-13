import argparse
import csv
from time import perf_counter

from solver import Grid, grid_to_string, parse_grid, solve_all
from strategies import STRATEGIES


def mirror_horizontal(grid: Grid) -> Grid:
    return [list(reversed(row)) for row in grid]


def mirror_vertical(grid: Grid) -> Grid:
    return list(reversed([row[:] for row in grid]))


def rotate_180(grid: Grid) -> Grid:
    return [list(reversed(row)) for row in reversed(grid)]


def variants(grid: Grid) -> list[tuple[str, Grid]]:
    return [
        ("original", [row[:] for row in grid]),
        ("mirror_horizontal", mirror_horizontal(grid)),
        ("mirror_vertical", mirror_vertical(grid)),
        ("rotate_180", rotate_180(grid)),
    ]


def analyze_csv(input_path: str, output_path: str, strategy: str = "mrv", max_solutions: int | None = 2) -> None:
    selector = STRATEGIES[strategy]

    with open(input_path, newline="", encoding="utf-8") as src, open(output_path, "w", newline="", encoding="utf-8") as dst:
        reader = csv.DictReader(src)
        fieldnames = [
            "id",
            "difficulty",
            "variant",
            "grid",
            "solutions_found",
            "attempts",
            "recursive_calls",
            "backtracks",
            "time_seconds",
        ]
        writer = csv.DictWriter(dst, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            grid = parse_grid(row["grid"])
            for variant_name, variant_grid in variants(grid):
                start = perf_counter()
                solutions, stats = solve_all(variant_grid, selector, max_solutions=max_solutions)
                elapsed = perf_counter() - start

                writer.writerow(
                    {
                        "id": row.get("id", ""),
                        "difficulty": row.get("difficulty", ""),
                        "variant": variant_name,
                        "grid": grid_to_string(variant_grid),
                        "solutions_found": len(solutions),
                        "attempts": stats.attempts,
                        "recursive_calls": stats.recursive_calls,
                        "backtracks": stats.backtracks,
                        "time_seconds": f"{elapsed:.6f}",
                    }
                )


def main() -> None:
    parser = argparse.ArgumentParser(description="Analiza vzorca sudokujev za raziskovalno nalogo.")
    parser.add_argument("input", help="Vhodni CSV s stolpci id,difficulty,grid")
    parser.add_argument("-o", "--output", default="results.csv", help="Izhodni CSV")
    parser.add_argument("--strategy", choices=STRATEGIES.keys(), default="mrv")
    parser.add_argument("--max-solutions", type=int, default=2, help="Koliko rešitev največ iščemo; 2 zadošča za razvrstitev 0/1/več")
    args = parser.parse_args()

    analyze_csv(args.input, args.output, args.strategy, args.max_solutions)
    print(f"Rezultati zapisani v {args.output}")


if __name__ == "__main__":
    main()

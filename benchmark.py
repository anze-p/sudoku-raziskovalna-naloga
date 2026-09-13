from time import perf_counter

from solver import parse_grid, solve_first
from strategies import STRATEGIES


EXAMPLE = parse_grid(
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


def main() -> None:
    print("Primerjava strategij\n")
    for name, selector in STRATEGIES.items():
        start = perf_counter()
        solution, stats = solve_first(EXAMPLE, selector)
        elapsed = perf_counter() - start

        print(f"Strategija: {name}")
        print(f"Rešitev najdena: {'da' if solution else 'ne'}")
        print(f"Poskusi: {stats.attempts}")
        print(f"Rekurzivni klici: {stats.recursive_calls}")
        print(f"Povratki: {stats.backtracks}")
        print(f"Čas: {elapsed:.6f} s\n")


if __name__ == "__main__":
    main()

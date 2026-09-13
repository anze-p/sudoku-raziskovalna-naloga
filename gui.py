import tkinter as tk
from tkinter import messagebox, ttk

from solver import is_valid_initial_grid, solve_all
from strategies import STRATEGIES


class SudokuGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Sudoku – raziskovalna naloga")

        self.entries: list[list[tk.Entry]] = []
        self.original: list[list[int]] = [[0] * 9 for _ in range(9)]
        self.solutions: list[list[list[int]]] = []
        self.solution_index = 0

        board = tk.Frame(root)
        board.pack(padx=12, pady=12)

        vcmd = (root.register(self.validate_cell), "%P")

        for r in range(9):
            row_entries = []
            for c in range(9):
                entry = tk.Entry(
                    board,
                    width=2,
                    justify="center",
                    font=("Segoe UI", 18),
                    validate="key",
                    validatecommand=vcmd,
                    relief="solid",
                    bd=1,
                )
                entry.grid(row=r, column=c, ipadx=7, ipady=5, padx=(2 if c % 3 == 0 else 0, 2), pady=(2 if r % 3 == 0 else 0, 2))
                row_entries.append(entry)
            self.entries.append(row_entries)

        controls = tk.Frame(root)
        controls.pack(pady=(0, 8))

        tk.Button(controls, text="Preveri", command=self.check).grid(row=0, column=0, padx=4)
        tk.Button(controls, text="Reši", command=self.solve).grid(row=0, column=1, padx=4)
        tk.Button(controls, text="Počisti", command=self.clear).grid(row=0, column=2, padx=4)

        self.strategy_var = tk.StringVar(value="mrv")
        ttk.Combobox(
            controls,
            textvariable=self.strategy_var,
            values=list(STRATEGIES.keys()),
            state="readonly",
            width=9,
        ).grid(row=0, column=3, padx=8)

        nav = tk.Frame(root)
        nav.pack(pady=(0, 10))
        self.prev_btn = tk.Button(nav, text="←", command=self.previous_solution, state="disabled")
        self.prev_btn.grid(row=0, column=0, padx=4)
        self.status = tk.Label(nav, text="Vnesi sudoku.")
        self.status.grid(row=0, column=1, padx=8)
        self.next_btn = tk.Button(nav, text="→", command=self.next_solution, state="disabled")
        self.next_btn.grid(row=0, column=2, padx=4)

    @staticmethod
    def validate_cell(value: str) -> bool:
        return value == "" or (len(value) == 1 and value in "123456789")

    def read_grid(self) -> list[list[int]]:
        return [[int(e.get()) if e.get() else 0 for e in row] for row in self.entries]

    def check(self) -> None:
        grid = self.read_grid()
        if is_valid_initial_grid(grid):
            messagebox.showinfo("Preverjanje", "Začetno stanje je veljavno.")
        else:
            messagebox.showerror("Preverjanje", "Začetno stanje ni veljavno.")

    def solve(self) -> None:
        grid = self.read_grid()
        if not is_valid_initial_grid(grid):
            messagebox.showerror("Napaka", "Začetno stanje ni veljavno.")
            return

        self.original = [row[:] for row in grid]
        self.solutions, stats = solve_all(grid, STRATEGIES[self.strategy_var.get()])
        self.solution_index = 0

        if not self.solutions:
            self.status.config(text="Sudoku nima rešitve.")
            self.update_navigation()
            return

        self.show_solution()
        self.status.config(
            text=f"Rešitev 1/{len(self.solutions)} | poskusi: {stats.attempts} | povratki: {stats.backtracks}"
        )
        self.update_navigation()

    def show_solution(self) -> None:
        solution = self.solutions[self.solution_index]
        for r in range(9):
            for c in range(9):
                entry = self.entries[r][c]
                entry.delete(0, tk.END)
                entry.insert(0, str(solution[r][c]))
                entry.config(fg="red" if self.original[r][c] else "black")
        self.status.config(text=f"Rešitev {self.solution_index + 1}/{len(self.solutions)}")

    def update_navigation(self) -> None:
        multi = len(self.solutions) > 1
        self.prev_btn.config(state="normal" if multi else "disabled")
        self.next_btn.config(state="normal" if multi else "disabled")

    def previous_solution(self) -> None:
        if not self.solutions:
            return
        self.solution_index = (self.solution_index - 1) % len(self.solutions)
        self.show_solution()

    def next_solution(self) -> None:
        if not self.solutions:
            return
        self.solution_index = (self.solution_index + 1) % len(self.solutions)
        self.show_solution()

    def clear(self) -> None:
        self.solutions = []
        self.solution_index = 0
        self.original = [[0] * 9 for _ in range(9)]
        for row in self.entries:
            for entry in row:
                entry.delete(0, tk.END)
                entry.config(fg="black")
        self.status.config(text="Vnesi sudoku.")
        self.update_navigation()


if __name__ == "__main__":
    root = tk.Tk()
    SudokuGUI(root)
    root.mainloop()

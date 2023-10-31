import tkinter as tk
from tkinter.ttk import Notebook
from generator_interface import GenerationTab
from solver_interface import SolveTab
import sudoku


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku Generator & Solver")
        self.grid = sudoku.Grid()
        self.tab_control = Tabs(self, self.grid)
        self.tab_control.generation_tab.generate_puzzle()


class Tabs(Notebook):
    def __init__(self, root: MainWindow, grid: sudoku.Grid):
        super().__init__(root)
        self.generation_tab = GenerationTab(self, grid)
        self.add(self.generation_tab, text='Generate')
        self.solve_tab = SolveTab(self, grid)
        self.add(self.solve_tab, text='Solve')
        self.pack()
        self.generation_tab.export.solve.bind("<Button>", self.solve_generated_puzzle)

    def solve_generated_puzzle(self, _):
        self.select(self.solve_tab)
        self.solve_tab.grid = self.generation_tab.grid
        self.solve_tab.solve()


if __name__ == "__main__":
    window = MainWindow()
    window.mainloop()

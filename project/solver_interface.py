import tkinter as tk
from tkinter.ttk import Notebook, Frame, Label, Button
import sudoku


class SolveTab(Frame):
    def __init__(self, master_tabs: Notebook, grid: sudoku.Grid):
        super().__init__(master_tabs, padding=10)
        self.grid = grid
        self.inputs = Inputs(self)
        self.inputs.import_button.bind("<ButtonRelease>", self.import_file)
        self.inputs.solve_button.bind("<ButtonRelease>", self.solve)
        self.canvas = sudoku.SudokuCanvas(self)
        self.pen = sudoku.SudokuPen(self.canvas)

    def draw_grid(self, show_difficulty):
        self.pen.draw_grid(self.grid, show_difficulty)

    def import_file(self, _):
        self.grid.csv_to_data()
        self.draw_grid(show_difficulty=True)

    def solve(self, _=None):
        self.grid.solve_grid(get_first_solution=True)
        self.draw_grid(show_difficulty=False)


class Inputs(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.import_button = ImportButton(self)
        self.import_button.pack(side="left")
        Label(self).pack(side="left", expand=True, fill="x")
        self.solve_button = Button(self, text="Solve")
        self.solve_button.pack(side="left")
        self.pack(side="top", fill="x")


class ImportButton(Button):
    def __init__(self, master):
        super().__init__(master, text='Open CSV File')
        self.filename = tk.StringVar()

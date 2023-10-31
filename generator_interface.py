import tkinter as tk
from tkinter.ttk import Notebook, Frame, Label, Button, OptionMenu
from turtle import RawTurtle
import sudoku
from sudoku import BEGINNER, EASY, NORMAL, HARD, EXPERT


class GenerationTab(Frame):
    def __init__(self, master_tabs: Notebook, grid: sudoku.Grid):
        super().__init__(master_tabs, padding=10)
        self.grid = grid
        self.inputs = Inputs(self)
        self.inputs.generate_button.bind("<Button>", self.generate_puzzle)
        self.canvas = sudoku.SudokuCanvas(self)
        self.status_label = GenerationStatusLabel(self)
        self.pen = RawTurtle(self.canvas)
        sudoku.turtle_setup(self.pen)
        self.export = Export(self)
        self.export.csv.bind("<Button>", self.export_puzzle)

    def generate_puzzle(self, _=None):
        self.status_label.status.set("Status: Generating...")
        self.grid = sudoku.generate_puzzle(self.pen, self.inputs.difficulty_selector.difficulty)
        self.status_label.status.set("Status: Complete")

    def export_puzzle(self, _):
        self.grid.save_data()


class Inputs(Frame):
    def __init__(self, master):
        super().__init__(master)
        Label(self, text="Difficulty:").pack(side="left")
        self.difficulty_selector = DifficultyMenu(self)
        self.difficulty_selector.pack(side="left")
        Label(self).pack(side="left", expand=True, fill="x")
        self.generate_button = Button(self, text="Generate")
        self.generate_button.pack(side="left")
        self.pack(side="top", fill="x")


class DifficultyMenu(OptionMenu):
    def __init__(self, master):
        self.options = ["Beginner", "Easy", "Normal", "Hard", "Expert"]
        self.value = tk.StringVar(value="Normal")
        self.difficulty = NORMAL
        super().__init__(master, self.value, None, *self.options, command=self.set_difficulty)

    def set_difficulty(self, _):
        index = [i for i, s in enumerate(self.options) if s == self.value.get()][0]
        difficulty_list = [BEGINNER, EASY, NORMAL, HARD, EXPERT]
        self.difficulty = difficulty_list[index]


class GenerationStatusLabel(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.status = tk.StringVar(value="Status: Idle")
        self.label = Label(self, textvariable=self.status)
        self.label.pack(side="left")
        self.pack(side="top", fill="x")


class Export(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.csv = Button(self, text="Export to CSV")
        self.csv.pack(side="left")
        self.pack(side="top", fill="x")
        Label(self).pack(side="left", expand=True, fill="x")
        self.solve = Button(self, text="Solve")
        self.solve.pack(side="left")

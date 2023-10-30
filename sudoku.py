from turtle import Turtle
from random import shuffle
from time import sleep
from copy import deepcopy


class DIM:
    CELL = 30
    LEFT = -CELL * 9 / 2
    TOP = CELL * 9 / 2
    RIGHT = CELL * 9 / 2
    BOTTOM = -CELL * 9 / 2


class DIFFICULTY:
    def __init__(self, max_failed_attempts, min_num_hints):
        self.max_failed_attempts = max_failed_attempts
        self.min_num_hints = min_num_hints

    @staticmethod
    def estimate(num_hints):
        if num_hints >= 45:
            return "BEGINNER"
        elif num_hints >= 40:
            return "EASY"
        elif num_hints >= 35:
            return "NORMAL"
        elif num_hints >= 30:
            return "HARD"
        else:
            return "EXPERT"


BEGINNER = DIFFICULTY(1, 45)
EASY = DIFFICULTY(3, 40)
NORMAL = DIFFICULTY(5, 35)
HARD = DIFFICULTY(10, 30)
EXPERT = DIFFICULTY(18, 17)


def flatten_list_of_lists(lst):
    return [item for sublist in lst for item in sublist]


class Grid:
    def __init__(self):
        self.data = [[0] * 9 for _ in range(9)]
        self.generate_solved_grid()
        self.backup = {"row": 0, "col": 0, "val": 0}

    def at(self, row, col):
        return self.data[row][col]

    def empty_at(self, val_row, val_col):
        return self.at(val_row, val_col) == 0

    def set_value(self, val_row, val_col, value):
        self.data[val_row][val_col] = value

    def clear_cell(self, row, col):
        self.set_value(row, col, 0)

    def get_first_empty_cell(self):
        for row in range(9):
            for column in range(9):
                if self.empty_at(row, column):
                    return row, column

    def set_backup(self, row, col, value):
        self.backup.update(row=row, col=col, val=value)

    def restore_backup(self):
        self.set_value(self.backup.get("row"), self.backup.get("col"), self.backup.get("val"))

    def clear_rand_cell(self):
        # Include list of all filled cells
        filled_cells = [(row, col) for row in range(9) for col in range(9) if not self.empty_at(row, col)]
        # Add another entry for cells in rows with more than 5 filled cells
        for row_num in range(9):
            row = [(row_num, col_num) for col_num in range(9) if not self.empty_at(row_num, col_num)]
            filled_cells.extend(row) if len(row) > 5 else None
        # Add another entry for cells in columns with more than 5 filled cells
        for col_num in range(9):
            column = [(row_num, col_num) for row_num in range(9) if not self.empty_at(row_num, col_num)]
            filled_cells.extend(column) if len(column) > 5 else None
        # Add another entry for cells in 3x3 squares with more than 5 filled cells
        for x, y in [(x, y) for x in range(3) for y in range(3)]:
            square_cells = [(i + x * 3, j + y * 3) for i in range(3) for j in range(3)]
            filled_square_cells = [(rn, cn) for rn, cn in square_cells if self.empty_at(rn, cn)]
            filled_cells.extend(filled_square_cells) if len(filled_square_cells) > 5 else None
        # Shuffle list and select the first one
        shuffle(filled_cells)
        rand_cell = filled_cells[0]
        self.set_backup(*rand_cell, self.at(*rand_cell))
        self.clear_cell(*rand_cell)

    def row(self, val_row):
        return self.data[val_row]

    def column(self, val_col):
        return [self.at(row, val_col) for row in range(9)]

    def square(self, val_row, val_col):
        rows = [i + (val_row // 3) * 3 for i in range(0, 3)]
        columns = [j + (val_col // 3) * 3 for j in range(0, 3)]
        return [[self.at(r, c) for c in columns] for r in rows]

    def check_full_grid(self):
        return 0 not in flatten_list_of_lists(self.data)

    def get_num_hints(self):
        return len([val for val in flatten_list_of_lists(self.data) if val != 0])

    def validate_row(self, val_row, value):
        return value not in self.row(val_row)

    def validate_column(self, val_col, value):
        return value not in self.column(val_col)

    def validate_square(self, val_row, val_col, value):
        return value not in flatten_list_of_lists(self.square(val_row, val_col))

    def validate_value(self, val_row, val_col, value):
        row_valid = self.validate_row(val_row, value)
        column_valid = self.validate_column(val_col, value)
        square_valid = self.validate_square(val_row, val_col, value)
        return row_valid and column_valid and square_valid

    def generate_solved_grid(self):
        number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        shuffle(number_list)
        location = self.get_first_empty_cell()
        for value in number_list:
            if self.validate_value(*location, value):
                self.set_value(*location, value)
                if self.check_full_grid() or self.generate_solved_grid():
                    return True
        self.clear_cell(*location)
        return False

    def solve_grid(self, num_solutions=0):
        location = self.get_first_empty_cell()
        for valid_value in [value for value in range(1, 10) if self.validate_value(*location, value)]:
            self.set_value(*location, valid_value)
            if self.check_full_grid():
                num_solutions += 1
                if num_solutions > 1:
                    return True, num_solutions
                else:
                    break
            else:
                solved, num_solutions = self.solve_grid(num_solutions)
                if solved:
                    return True, num_solutions
        self.clear_cell(*location)
        return False, num_solutions


def write_text(pen: Turtle, message, x, y, align="left", font_size=18):
    pen.up()
    pen.goto(x, y)
    pen.write(message, align=align, font=('Arial', font_size, 'normal'))


def draw_grid(pen: Turtle, grid: Grid):
    def draw_val(val_row, val_col):
        x = DIM.LEFT + val_col * DIM.CELL + DIM.CELL / 2
        y = DIM.TOP - val_row * DIM.CELL - DIM.CELL * 1
        write_text(pen, grid.at(row, col), x, y, align="center")

    pen.clear()
    for row in range(0, 10):
        pen.pensize(3 if (row % 3) == 0 else 1)
        pen.up()
        pen.goto(DIM.LEFT, DIM.TOP - row * DIM.CELL)
        pen.down()
        pen.goto(DIM.LEFT + 9 * DIM.CELL, DIM.TOP - row * DIM.CELL)
    for col in range(0, 10):
        pen.pensize(3 if (col % 3) == 0 else 1)
        pen.up()
        pen.goto(DIM.LEFT + col * DIM.CELL, DIM.TOP)
        pen.down()
        pen.goto(DIM.LEFT + col * DIM.CELL, DIM.TOP - 9 * DIM.CELL)
    for row, col in [(row, col) for row in range(9) for col in range(9) if not grid.empty_at(row, col)]:
        draw_val(row, col)
    write_text(pen, "Difficulty: " + DIFFICULTY.estimate(grid.get_num_hints()), DIM.LEFT, DIM.TOP + 8, font_size=8)
    pen.getscreen().update()


# Generate a fully solved puzzle
def generate_puzzle(pen: Turtle, difficulty: DIFFICULTY):
    grid = Grid()
    draw_grid(pen, grid)
    sleep(1)

    failed_attempts = 0
    num_hints = 81
    while failed_attempts < difficulty.max_failed_attempts and num_hints > difficulty.min_num_hints:
        grid.clear_rand_cell()
        grid_copy = deepcopy(grid)
        _, num_solutions = grid_copy.solve_grid()
        if num_solutions != 1:
            grid.restore_backup()
            failed_attempts += 1
            print("failed attempt", failed_attempts)
        else:
            num_hints = grid.get_num_hints()
            draw_grid(pen, grid)

    print("Number of hints:", num_hints)
    print("Puzzle generation complete")


def turtle_setup(pen: Turtle):
    pen.getscreen().tracer(0)
    pen.speed(0)
    pen.color("black")
    pen.hideturtle()


def animate_puzzle_generation():
    pen = Turtle()
    turtle_setup(pen)
    generate_puzzle(pen, NORMAL)
    pen.getscreen().mainloop()


# Run this file for Turtle only
if __name__ == "__main__":
    animate_puzzle_generation()

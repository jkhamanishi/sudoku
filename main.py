import turtle
from random import randint, shuffle
from time import sleep


class DIM:
    LEFT = -150
    TOP = 150
    RIGHT = 150
    BOTTOM = -150
    CELL = 30




def draw_grid(pen, grid):
    turtle.tracer(0)
    pen.speed(0)
    pen.color("#000000")
    pen.hideturtle()

    def draw_text(message, x, y):
        pen.up()
        pen.goto(x, y)
        pen.write(message, align="center", font=('Arial', 18, 'normal'))

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
    for row in range(0, 9):
        for col in range(0, 9):
            if grid[row][col] != 0:
                draw_text(grid[row][col], DIM.LEFT + col * DIM.CELL + DIM.CELL / 2, DIM.TOP - row * DIM.CELL - DIM.CELL)


# A function to check if the grid is full
def check_full_grid(grid):
    for row in range(0, 9):
        for col in range(0, 9):
            if grid[row][col] == 0:
                return False
    return True


# A backtracking/recursive function to check all possible combinations of numbers until a solution is found
def solve_grid(grid, num_solutions=0):
    # Find next empty cell
    row = col = 0
    for i in range(0, 81):
        row = i // 9
        col = i % 9
        if grid[row][col] == 0:
            for value in range(1, 10):
                # Check that this value has not already be used on this row
                if not (value in grid[row]):
                    # Check that this value has not already be used on this column
                    if value not in [grid[r][col] for r in range(9)]:
                        # Identify which of the 9 squares we are working on
                        square = []
                        if row < 3:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(0, 3)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(0, 3)]
                            else:
                                square = [grid[i][6:9] for i in range(0, 3)]
                        elif row < 6:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(3, 6)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(3, 6)]
                            else:
                                square = [grid[i][6:9] for i in range(3, 6)]
                        else:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(6, 9)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(6, 9)]
                            else:
                                square = [grid[i][6:9] for i in range(6, 9)]
                        # Check that this value has not already be used on this 3x3 square
                        if not value in (square[0] + square[1] + square[2]):
                            grid[row][col] = value
                            if check_full_grid(grid):
                                num_solutions += 1
                                break
                            else:
                                solved, num_solutions = solve_grid(grid, num_solutions)
                                if solved:
                                    return True, num_solutions
            break
    grid[row][col] = 0
    return False, num_solutions


numberList = [1, 2, 3, 4, 5, 6, 7, 8, 9]


# A backtracking/recursive function to check all possible combinations of numbers until a solution is found
def fill_grid(grid):
    row = col = 0
    # Find next empty cell
    for i in range(0, 81):
        row = i // 9
        col = i % 9
        if grid[row][col] == 0:
            shuffle(numberList)
            for value in numberList:
                # Check that this value has not already be used on this row
                if not (value in grid[row]):
                    # Check that this value has not already be used on this column
                    if value not in [grid[r][col] for r in range(9)]:
                        # Identify which of the 9 squares we are working on
                        square = []
                        if row < 3:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(0, 3)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(0, 3)]
                            else:
                                square = [grid[i][6:9] for i in range(0, 3)]
                        elif row < 6:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(3, 6)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(3, 6)]
                            else:
                                square = [grid[i][6:9] for i in range(3, 6)]
                        else:
                            if col < 3:
                                square = [grid[i][0:3] for i in range(6, 9)]
                            elif col < 6:
                                square = [grid[i][3:6] for i in range(6, 9)]
                            else:
                                square = [grid[i][6:9] for i in range(6, 9)]
                        # Check that this value has not already be used on this 3x3 square
                        if not value in (square[0] + square[1] + square[2]):
                            grid[row][col] = value
                            if check_full_grid(grid):
                                return True
                            else:
                                if fill_grid(grid):
                                    return True
            break
    grid[row][col] = 0


# Generate a Fully Solved Grid
def generate_puzzle():
    # initialise empty 9 by 9 grid
    grid = [[0 for column in range(9)] for row in range(9)]

    # initialize turtle
    pen = turtle.Turtle()
    fill_grid(grid)
    draw_grid(pen, grid)
    pen.getscreen().update()
    sleep(1)

    # Start Removing Numbers one by one

    # A higher number of attempts will end up removing more numbers from the grid
    # Potentially resulting in more difficult grids to solve!
    max_failed_attempts = 5
    failed_attempts = 0
    while failed_attempts < max_failed_attempts:
        # Select a random cell that is not already empty
        row = randint(0, 8)
        col = randint(0, 8)
        while grid[row][col] == 0:
            row = randint(0, 8)
            col = randint(0, 8)
        # Remember its cell value in case we need to put it back
        backup = grid[row][col]
        grid[row][col] = 0

        # Take a full copy of the grid
        copy_grid = []
        for r in range(0, 9):
            copy_grid.append([])
            for c in range(0, 9):
                copy_grid[r].append(grid[r][c])

        # Count the number of solutions that this grid has
        _, num_solutions = solve_grid(copy_grid)
        if num_solutions != 1:
            grid[row][col] = backup  # revert change
            failed_attempts += 1

        pen.clear()
        draw_grid(pen, grid)
        pen.getscreen().update()

    print("Puzzle Creation Complete")
    pen.getscreen().mainloop()





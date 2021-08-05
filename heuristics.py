from game_state import Game
from blocks import Block


def find_highest_cell(game: Game):
    highest_cells = {}
    for row in range(10):
        for col in range(10):
            if game.board[row][col] and col not in highest_cells:
                highest_cells[col] = row
    return highest_cells


def find_hole_1(game: Game):
    """
    finds empty cells to the left/right of a column in which the topmost cell is at the same height or
    above the empty cell - we will name it a hole of type 1
    :return: num of holes of type 1
    """
    holes = []  # TODO if want to add another hole type - repeating index = right + left
    for row in range(10):
        for col in range(10):
            if col < 9:
                if not game.board[row][col] and game.highest_cells[col + 1] <= row:
                    holes.append((row, col))
            if col > 1:
                if not game.board[row][col] and game.highest_cells[col - 1] <= row:
                    holes.append((row, col))
    return len(holes)


def find_hole_2(game: Game):
    """
    finds empty cells under the topmost filled cell in the same column - we will name it a hole of type 2
    :return: num of holes of type 2
    """
    holes = []
    for row in range(10):
        for col in range(10):
            if not game.board[row][col] and game.highest_cells[col] <= row:
                holes.append((row, col))
    return len(holes)


def fixed_func(game: Game, hole_type):
    """
     each hole of type i={1,2} is given a score 1
    """
    if hole_type == 1:
        return find_hole_1(game)
    return find_hole_2(game)


def identity_func(game: Game, hole_type):
    """
    each hole of type i={1,2} is given the identity score
    """
    if hole_type == 1:
        return find_hole_1(game)
    return 2 * find_hole_2(game)


def square_func(game: Game, hole_type):
    if hole_type == 1:
        find_hole_1_score = find_hole_1(game)
        return find_hole_1_score ** 2
    find_hole_2_score = find_hole_2(game)
    return find_hole_2_score ** 2

############
# best score:

def is_filling_row(game: Game):
    num_of_filled_rows = 0
    for row in range(10):
        if sum(game.board[row]) == 10:
            num_of_filled_rows += 1
    return num_of_filled_rows


def is_filling_col(game: Game):
    filled_cols = [0 for i in range(10)]
    for row in range(10):
        for col in range(10):
            if game.board[row][col]:
                filled_cols[col] += 1

    num_of_filled_cols = 0
    for col in filled_cols:
        if col == 10:
            num_of_filled_cols += 1
    return num_of_filled_cols


def filling_score_1(game: Game):
    num_of_filled_cols = is_filling_col(game)
    num_of_filled_rows = is_filling_row(game)
    return num_of_filled_cols + num_of_filled_rows


def filling_score_2(game: Game):
    num_of_filled_cols = is_filling_col(game)
    num_of_filled_rows = is_filling_row(game)
    return (num_of_filled_cols * num_of_filled_cols) + num_of_filled_rows


def filling_score_3(game: Game):
    num_of_filled_cols = is_filling_col(game)
    num_of_filled_rows = is_filling_row(game)
    return num_of_filled_cols + (num_of_filled_rows * num_of_filled_rows)


def filling_score_4(game: Game):
    num_of_filled_cols = is_filling_col(game)
    num_of_filled_rows = is_filling_row(game)
    return max(num_of_filled_cols, num_of_filled_rows)

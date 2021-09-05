from game_state import Game
import numpy as np
from blocks import Block, BLOCKS
from action import Action

TOTAL_COORDINATES = 10 * 10
ALL_BLOCKS = BLOCKS()
BLOCKS_LIST = ALL_BLOCKS.block_list
LARGE_SQUARE_BLOCK = Block(len(BLOCKS_LIST) - 1, BLOCKS(), None, False)
CORNERS = [(0, 0), (0, 9), (9, 0), (9, 9)]

def free_space_heuristic(game_state: Game):
	return TOTAL_COORDINATES - np.sum(game_state.board)

def empty_large_square_heuristic(game_state: Game):
	if len(game_state.get_legal_actions(LARGE_SQUARE_BLOCK)) > 0:
		return 0
	else:
		return -100000

def one_square_hole(game_state: Game):
	holes = 0
	for row in range(len(game_state.board)):
		for col in range(len(game_state.board)):
			if not game_state.board[row][col]:
				around = 4
				for coord in one_square_hole_helper(row, col):
					if coord[0] < 0 or coord[0] > 9 or coord[1] < 0 or coord[1] > 9:
						around -= 1
					else:
						around -= game_state.board[coord[0]][coord[1]]
				if around == 0:
					holes += 1
	return - holes

def one_square_hole_helper(row, col):
	return [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

def surface_heuristic(game_state: Game, action: Action):
	surface_filled = set()
	for block_col, block_row in action.block.coord_array:
		for row, col in one_square_hole_helper(block_row + action.y, block_col + action.x):
			if (row, col) not in surface_filled:
				if row < 0 or row > 9 or col < 0 or col > 9:
					surface_filled.add((row, col))
				elif game_state.board[row][col] == 1:
					surface_filled.add((row, col))
	return len(surface_filled)


def row_col_completeness_heuristic(game_state: Game, action: Action):
	successor = game_state.generate_successor(action, clear_line=False)
	cols = np.sum(successor.board, axis=0)
	rows = np.sum(successor.board, axis=1)
	cols *= cols
	rows *= rows
	result = (np.sum(cols) + np.sum(rows)) / np.sum(successor.board)
	return result


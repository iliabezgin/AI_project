from game_state import Game
import numpy as np
from blocks import Block, BLOCKS

TOTAL_COORDINATES = 10 * 10
ALL_BLOCKS = BLOCKS()
BLOCKS_LIST = ALL_BLOCKS.block_list
LARGE_SQUARE_BLOCK = Block(len(BLOCKS_LIST) - 1, BLOCKS(), None, False)


def board_heuristic_1(game_state: Game):
	return 100 * (TOTAL_COORDINATES - np.sum(game_state.board))

def board_heuristic_2(game_state: Game):
	return 1000 * (game_state.board[0][0] + game_state.board[0][9])

#+ game_state.board[9][0]  + game_state.board[9][9]

def empty_large_square_heuristic(game_state: Game):
	enough_space = False
	if len(game_state.get_legal_actions(LARGE_SQUARE_BLOCK)) > 0:
		# TODO give normal score
		pass
	else:
		#TODO give very low score
		pass

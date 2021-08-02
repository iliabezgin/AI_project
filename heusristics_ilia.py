from game_state import Game
import numpy as np

TOTAL_COORDINATES = 10 * 10

def board_heuristic_1(game_state: Game):
	return (TOTAL_COORDINATES - np.sum(game_state.board)) % 10

import argparse
import game_1010_main
from agents import *
from game_state import Game
from heusristics_ilia import *
from heuristics import *
import pandas as pd
import time

fs = 1
os = 50
s = 2.5
rcc = 0.5



def test_board_heuristic(game_state: Game):
	free_space = free_space_heuristic(game_state) # 50-80
	one_square = one_square_hole(game_state) # -(0-5)
	empty_large_square = empty_large_square_heuristic(game_state) # -100000
	val = fs * free_space + os * one_square + empty_large_square
	return val

def test_board_action_heuristic(game_state: Game, action):
	surface = surface_heuristic(game_state, action) # 0-9
	row_col_completeness = row_col_completeness_heuristic(game_state, action) # 5-12
	val = s * surface + rcc * row_col_completeness
	return val

def test_block_heuristic(game_state: Game, block):
	return -len(block.coord_array)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='1010! game.')
	agents = ['HumanAgent', 'GreedyBFSSingleAgent', 'GreedyBFSTripleAgent', 'AlphaBetaAgent',
			  'AlphaBetaAgentV2', 'AlphaBetaAgentV3']
	parser.add_argument('--agent', choices=agents, help='The agent.', default=agents[0], type=str)
	parser.add_argument('--sleep', help='Does sleep between actions', default=False, action='store_true')
	parser.add_argument('--gui', help='Whether to turn GUI on', default=False, action='store_true')
	parser.add_argument('--repeat', help='The number of repetitions of the hole game', default=1, type=int)
	parser.add_argument('--output', help='Path to output directory (with \"/\" at the end)', default=None)
	parser.add_argument('--version', help='The version of the alpha-beta algorithm (1, 2, 3)', default=2, type=int)
	parser.add_argument('--depth', help='The depth of alpha-beta algorithm run', default=0, type=int)


	args = parser.parse_args()

	points = []
	speed_list = []
	for repetition in range(args.repeat):
		start = time.time()
		agent = AgentFactory.create_agent(args.agent, test_board_heuristic, test_board_action_heuristic,
										  test_block_heuristic, args.version, args.depth)
		main_game = game_1010_main.Main(agent=agent, sleep_between_actions=args.sleep, has_gui=args.gui)
		points.append(main_game.points)
		main_game.destroy()
		duration = time.time() - start
		speed = main_game.turns / (duration / 60)
		speed_list.append(speed)
		print(f"Points: {main_game.points}")
		print(f"Time: {duration}")
		print(f"Turns per min: {speed}")
	print(args.agent)
	print(points)
	print(f"Average points after {args.repeat} repetitions: {sum(points)/args.repeat}")
	if args.output is not None:
		df = pd.DataFrame([points, speed_list])
		path = f"{args.output}{args.agent}_fs{fs}_os{os}_s{s}_rcc{rcc}_rpt{args.repeat}.csv"
		df.to_csv(path, index=False, header=False)

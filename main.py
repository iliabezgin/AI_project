import argparse
import game_1010_main
from agents import *
from game_state import Game
from heusristics_ilia import *
from heuristics import *
import time

def test_board_heuristic(game_state: Game):
	# Instead 0 should return your board heuristic function
	# val = square_func(game_state, 1) + board_heuristic_1(game_state) + board_heuristic_2(game_state)
	val = square_func(game_state, 2)

	# val = - filling_score_4(game_state)
	# print(val)
	return val
	# return 0

def test_block_heuristic(game_state: Game, block):
	# Instead 0 should return your block heuristic function
	return 0


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='1010! game.')
	agents = ['HumanAgent', 'ComputerAgent', 'SearchAgent', 'AlphaBetaAgent', 'MinmaxAgent']
	parser.add_argument('--agent', choices=agents, help='The agent.', default=agents[0], type=str)
	parser.add_argument('--sleep', help='Does sleep between actions', default=False, action='store_true')
	parser.add_argument('--repeat', help='The number of repetitions of the hole game', default=1, type=int)

	args = parser.parse_args()

	points = []
	for repetition in range(args.repeat):
		start = time.time()
		agent = AgentFactory.create_agent(args.agent, test_board_heuristic, test_block_heuristic)
		main_game = game_1010_main.Main(agent=agent, sleep_between_actions=args.sleep)
		points.append(main_game.points)
		main_game.destroy()
		duration = time.time() - start
		print(f"Time: {duration}")
		print(f"Turns per min: {main_game.turns / (duration / 60)}")
	print(args.agent)
	print(points)
	print(f"Average points after {args.repeat} repetitions: {sum(points)/args.repeat}")

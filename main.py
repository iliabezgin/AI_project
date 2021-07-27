import argparse
import game_1010_main
from agents import *
from game_state import Game
from heusristics_ilia import *

def test_board_heuristic(game_state: Game):
	# Instead 0 should return your board heuristic function
	return board_heuristic_1(game_state)
	# return 0

def test_block_heuristic(game_state: Game, block):
	# Instead 0 should return your block heuristic function
	return 0


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='1010! game.')
	agents = ['HumanAgent', 'ComputerAgent', 'SearchAgent']
	parser.add_argument('--agent', choices=agents, help='The agent.', default=agents[0], type=str)
	parser.add_argument('--sleep', help='Does sleep between actions', default=True, action='store_true')

	args = parser.parse_args()
	agent = AgentFactory.create_agent(args.agent, test_board_heuristic, test_block_heuristic)
	main = game_1010_main.Main(agent=agent, sleep_between_actions=args.sleep)
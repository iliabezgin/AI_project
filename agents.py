import abc
from game_state import Game
import numpy as np
from util import PriorityQueue


class Agent(object):
	def __init__(self):
		super(Agent, self).__init__()

	@abc.abstractmethod
	def get_action(self, game_state: Game):
		'''
		Returns action for the current game state
		:param game_state:
		'''
		return

	def stop_running(self):
		pass

	@abc.abstractmethod
	def get_type(self):
		return

class HumanAgent(Agent):

	def __init__(self):
		super().__init__()

	def get_action(self, game_state: Game):
		pass

	def get_type(self):
		return "HumanAgent"

class ComputerAgent(Agent):

	def __init__(self, board_heuristic, block_heuristic):
		super().__init__()
		self.board_heuristic = board_heuristic
		self.block_heuristic = block_heuristic

	def get_action(self, game_state: Game):
		ignore_list = []
		selected_block = self.select_block(game_state, ignore_list)
		legal_moves = game_state.get_legal_actions(selected_block)
		while len(legal_moves) == 0:
			ignore_list.append(selected_block)
			selected_block = self.select_block(game_state, ignore_list)
			legal_moves = game_state.get_legal_actions(selected_block)

		# Choose one of the best actions
		scores = [self.board_heuristic(game_state.generate_successor(action)) for action in legal_moves]
		best_score = max(scores)
		best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
		chosen_index = np.random.choice(best_indices)  # Pick randomly among the best

		return legal_moves[chosen_index]

	def select_block(self, game_state: Game, ignore_list):
		blocks_scores = []
		for block in game_state.current_blocks:
			if block not in ignore_list:
				blocks_scores.append(self.block_heuristic(game_state, block))
			else:
				blocks_scores.append(-1)
		block_index = np.argmax(blocks_scores)
		return game_state.current_blocks[block_index]

	def get_type(self):
		return "ComputerAgent"

class SearchAgent(Agent):
	def __init__(self, board_heuristic):
		super().__init__()
		self.board_heuristic = board_heuristic
		self.actions = []

	def get_action(self, game_state: Game):
		if len(self.actions) == 0:
			self.actions = self.a_star_search(game_state)
		if len(self.actions) == 0:
			self.actions = self.a_star_search(game_state)
		action = self.actions.pop(0)
		for block in game_state.current_blocks:
			if block.block_list_index == action.block.block_list_index:
				action.block = block
				break
		return action

	def get_type(self):
		return "SearchAgent"

	def a_star_search(self, game):
		"""
		Search the node that has the lowest combined cost and heuristic first.
		"""
		# return general_search(problem, util.PriorityQueue(), priority=True, heuristic=heuristic)
		fringe = PriorityQueue()
		start = True
		visited = set()
		current = Node(game, [])
		fringe.push(Node(game, []), 0)
		while not fringe.isEmpty():
			current = fringe.pop()
			if current.state not in visited:
				visited.add(current.state)
				if not start and len(current.state.current_blocks) == 3:
					return current.actions
				start = False
				for triplet in current.state.get_successors():
					fringe.push(Node(triplet[0], current.actions + [triplet[1]]), -self.board_heuristic(triplet[0]))
		return current.actions




class Node:
	def __init__(self, state, actions):
		self.state = state
		self.actions = actions

class AgentFactory():

	@staticmethod
	def create_agent(agent_name, test_board_heuristic, test_block_heuristic):
		if agent_name == "HumanAgent":
			return HumanAgent()
		if agent_name == "ComputerAgent":
			return ComputerAgent(test_board_heuristic, test_block_heuristic)
		if agent_name == "SearchAgent":
			return SearchAgent(test_board_heuristic)

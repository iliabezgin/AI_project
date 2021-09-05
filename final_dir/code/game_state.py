import random

from blocks import Block, BLOCKS
from action import *
from random import randint
# from hueristics import find_highest_cell

import copy
BOARD_SIZE = 10


class Game:
	def __init__(self, gui):
		self.gui = gui
		if gui is None:
			self.gui_for_blocks = False
		else:
			self.gui_for_blocks = True
		self.board = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # to get coordinate x, y call board[y][x]
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

		self.points = 0
		self.blocks = BLOCKS()
		self.current_blocks = []
		self.selected_block = None
		self.highest_cells = self.find_highest_cell()

	def apply_action(self, action: Action, clear_line: bool):
		'''
		Applies action on current board (without GUI)
		:param action: action to apply
		'''
		x = action.x
		y = action.y
		coordinates = action.block.coord_array
		if self.fits(x, y, coordinates):
			for index in range(0, len(coordinates)):
				self.set_filed(x + coordinates[index][0], y + coordinates[index][1], 1)
			for block in self.current_blocks:
				if block.block_list_index == action.block.block_list_index:
					self.current_blocks.remove(block)
					break
			if len(self.current_blocks) == 0:
				self.generate_blocks()

		if clear_line:
			lines = self.check_lines()
			columns = self.check_columns()
			total_to_clear = len(lines) + len(columns)
			if total_to_clear > 1:
				if total_to_clear == 2:
					self.add_points(10)
				elif total_to_clear == 3:
					self.add_points(30)
				elif total_to_clear == 4:
					self.add_points(60)
				elif total_to_clear == 5:
					self.add_points(100)
				elif total_to_clear == 6:
					self.add_points(150)

			if len(lines) > 0:
				for line in lines:
					self.clear_line(line)

			if len(columns) > 0:
				for columns in self.check_columns():
					self.clear_column(columns)


		self.update_highest_cells()

	def get_legal_actions(self, block: Block):
		'''
		:param block: block to place
		:return: all legal actions for current game state and given block
		'''
		board_size = len(self.board)
		actions = []
		for x in range(board_size - block.w + 1):
			for y in range(board_size - block.h + 1):
				if self.fits(x, y, block.coord_array):
					actions.append(Action(x, y, block))
		return actions

	def generate_successor(self, action: Action, clear_line: bool):
		'''
		Generate a new board state by applying given action
		:param action: action to apply
		:param clear_line: whether to clean the line when it is completed
		:return: a new game state
		'''
		successor = Game(None)
		successor.board = copy.deepcopy(self.board)
		successor.points = self.points
		successor.current_blocks = [Block(block.block_list_index, self.blocks, None, False) for block in self.current_blocks]
		successor.apply_action(action, clear_line=clear_line)
		return successor

	def get_successors(self):
		'''
		:return: all possible successors for the current board and current pieces
		'''
		successors = []
		for block in self.current_blocks:
			for action in self.get_legal_actions(block):
				successors.append((self.generate_successor(action, True), action))
		return successors

	def generate_successor_2(self, action: Action, size: int):
		'''
		Generate a new board state by applying given action (For alpha-beta algorithm)
		:return: a new game state
		'''
		if size>1:
			successor = Game(None)
			successor.board = copy.deepcopy(self.board)
			successor.current_blocks = [Block(block.block_list_index, self.blocks, None, False) for block in self.current_blocks]
			successor.apply_action(action, clear_line=True)
			return successor
		else:
			successor = Game(None)
			successor.board = copy.deepcopy(self.board)
			successor.current_blocks = self.current_blocks
			successor.apply_action(action, clear_line=True)
			successor.current_blocks = []
			return successor

	def check_lines(self):
		'''
		checks which rows are filled
		:return: indexes of filled rows
		'''
		lines = []
		for line in range(0, 10):
			flag = 1
			for i in range(0, 10):
				if self.board[line][i] != 1:
					flag = 0
					break
			if flag == 1:
				lines.append(line)
		return lines

	def check_columns(self):
		'''
		checks which columns are filled
		:return: indexes of filled columns
		'''
		columns = []
		for column in range(0, 10):
			flag = 1
			for i in range(0, 10):
				if self.board[i][column] != 1:
					flag = 0
					break
			if flag == 1:
				columns.append(column)
		return columns

	def get_points(self):
		'''
		:return: current game points
		'''
		return self.points

	def add_points(self, points):
		self.points += points
		if self.gui is not None:
			self.gui.points_label["text"] = str(self.points)
			self.gui.points_label.place(x=(300 - self.gui.points_label.winfo_width() / 2), y=10)

	def clear_line(self, index):
		for i in range(0, 10):
			self.set_filed(i, index, 0)

	def clear_column(self, index):
		for i in range(0, 10):
			self.set_filed(index, i, 0)

	def set_filed(self, x, y, full):
		self.add_points(1)
		self.board[y][x] = full

	def generate_blocks(self):
		'''
		Creates new triplet of pieces
		:return:
		'''
		self.current_blocks = []
		for i in range(0, 3):
			self.current_blocks.append(Block(random.choices(range(len(self.blocks.block_list)), weights=self.blocks.probabilities, k=1)[0],
											 self.blocks, self.gui, self.gui_for_blocks))


	def fits(self, x, y, coordinates):
		'''
		:param x: x coordinate
		:param y: y coordinate
		:param coordinates: piece's coordinates
		:return: True if the given piece could be placed on the board, False otherwise
		'''
		for index in range(0, len(coordinates)):
			tx = x + coordinates[index][0]
			ty = y + coordinates[index][1]

			if 0 <= tx < 10 and 0 <= ty < 10:
				if self.board[ty][tx] == 1:
					return False
			else:
				return False
		return True

	def is_action_possible(self):
		'''
		:return: True if exist at least one possible action for current board and current pieces
		False otherwise
		'''
		for y in range(0, len(self.board)):
			for x in range(0, len(self.board[y])):
				for block in self.current_blocks:
					if self.fits(x, y, block.coord_array):
						return True
		return False

	def find_highest_cell(self):
		# highest_cells = {}
		# for row in range(10):
		# 	for col in range(10):
		# 		if col not in highest_cells:
		# 			if self.board[row][col]:
		# 				highest_cells[col] = row
		# 			else:
		# 				highest_cells[col] = 9
		# return highest_cells
		pass

	def update_highest_cells(self):
		self.highest_cells = self.find_highest_cell()

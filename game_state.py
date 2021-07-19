from blocks import Block, BLOCKS
from action import *
from random import randint

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
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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

	def apply_action(self, action: Action):
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

		lines = self.check_lines()
		columns = self.check_columns()

		if len(lines) > 0:
			for line in lines:
				self.clear_line(line)

		if len(columns) > 0:
			for columns in self.check_columns():
				self.clear_column(columns)

	def get_legal_actions(self, block: Block):
		board_size = len(self.board)
		actions = []
		for x in range(board_size - block.h + 1):
			for y in range(board_size - block.w + 1):
				if self.fits(x, y, block.coord_array):
					actions.append(Action(x, y, block))
		return actions

	def generate_successor(self, action: Action):
		successor = Game(None)
		successor.board = copy.deepcopy(self.board)
		successor.current_blocks = [Block(block.block_list_index, self.blocks, None, False) for block in self.current_blocks]
		successor.apply_action(action)
		return successor

	def check_lines(self):
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
		return self.points

	def add_points(self, points):
		self.points += points
		self.gui.points_label["text"] = str(self.points)
		self.gui.points_label.place(x=(300 - self.gui.points_label.winfo_width() / 2), y=10)

	def clear_line(self, index):
		for i in range(0, 10):
			self.set_filed(i, index, 0)

	def clear_column(self, index):
		for i in range(0, 10):
			self.set_filed(index, i, 0)

	def set_filed(self, x, y, full):
		if self.gui is not None:
			self.add_points(1)
		self.board[y][x] = full

	def generate_blocks(self):
		self.current_blocks = []
		for i in range(0, 3):
			self.current_blocks.append(Block(randint(0, len(self.blocks.block_list) - 1), self.blocks, self.gui, self.gui_for_blocks))

	def fits(self, x, y, coordinates):
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
		for y in range(0, len(self.board)):
			for x in range(0, len(self.board[y])):
				for block in self.current_blocks:
					if self.fits(x, y, block.coord_array):
						return True
		return False
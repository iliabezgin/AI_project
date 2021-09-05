from blocks import Block


class Action:
	def __init__(self, x, y, block: Block):
		# x coordinate
		self.x = x
		# y coordinate
		self.y = y
		# block to be placed
		self.block = block

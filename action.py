from blocks import Block


class Action:
	def __init__(self, x, y, block: Block):
		self.x = x
		self.y = y
		self.block = block

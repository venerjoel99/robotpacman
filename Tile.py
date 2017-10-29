class Tile:

'''
Types (passed in as a string):
	Wall
	Space (no wall)
'''

	def __init__(self,type):
		self.type=type
		self.ghost=False
		self.pacman=False
		self.dot=False
		self.bigdot=False

	def hasGhost(self):
		return self.ghost

	def hasPacman(self):
		return self.pacman

	def hasDot(self):
		return self.dot

	def hasBigDot(self):
		return self.bigdot

	def getType(self):
		return self.type
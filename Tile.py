

class Tile:


	'''
	Types (passed in as a string):
		Wall
		Space (no wall)
		Unknown
	'''

	TYPECHARS=0






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

	def removeDot(self):
		self.dot=False
		self.bigdot=False


	def __str__(self):
		TYPECHARS={
		"Wall":"█",
		"Space":" ",
		"Dot": "·",
		"Unknown" : "X"}

		PACMAN="P"
		GHOST="G"

		if self.pacman:
			return PACMAN
		elif self.ghost:
			return GHOST
		else:
			return TYPECHARS[self.type]

if __name__=="__main__":
	t=Tile("Wall")
	print(t)

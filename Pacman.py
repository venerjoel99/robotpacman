class Pacman:

	START_LOCATION=(0,0)

	def __init__(self):
		x,y=Pacman.START_LOCATION
		self.setPosition(x,y)


	'''the maze passed into this will eventually be the pacbot's representation of the maze (from what it has seen so far)
	For now, the entire maze is passed into it
	'''
	def decideMove(self,maze): #return a string left right up or down
		pass

	def move(self,maze):
		m=self.decideMove(maze,ghosts)
		maze.movepacman(m)

	def getPosition(self):
		return self.x,self.y

	def setPosition(self,x,y): #only used at the beginning of the game/between deaths
		self.x=x
		self.y=y

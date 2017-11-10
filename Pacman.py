class Pacman:

	START_LOCATION=(0,0)

	def __init__(self):
		self.setPosition(START_LOCATION)


'''the maze passed into this will eventually be the pacbot's representation of the maze (from what it has seen so far)
For now, the entire maze is passed into it
'''
	def determineMove(self,maze,ghosts): #decide where to move








	def move(self,maze,direction):
		maze



'''

'''

	def getPosition(self):
		return self.x,self.y

	def setPosition(self,x,y): #only used at the beginning of the game/between deaths
		self.x=x
		self.y=y

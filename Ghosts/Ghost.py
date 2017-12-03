class Ghost:

	START_LOCATION=(0,0) #likely to be changed

	def __init__(self):
		x,y=Ghost.START_LOCATION
		self.setPosition(x,y)

	def move(self,maze):
		m=self.decidemove(maze)
		#maze.

	def decidemove(self,maze):
		pass

	def getPosition(self):
		return self.x,self.y

	def setPosition(self,x,y): #only used at the beginning of the game
		self.x=x
		self.y=y

	def kill(self): #when pacman passes over a ghost after a big dot is collected
		self.setPosition(START_LOCATION)

	def __str__(self):
		return "G"
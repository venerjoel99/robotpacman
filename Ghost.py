class Ghost:

	START_LOCATION=(0,0) #likely to be changed

	def __init__(self):
		self.setPosition(START_LOCATION)

	def move(self,maze):
		pass

	def getPosition(self):
		return self.x,self.y

	def setPosition(self,x,y): #only used at the beginning of the game
		self.x=x
		self.y=y

	def kill(self): #when pacman passes over a ghost after a big dot is collected
		self.setPosition(START_LOCATION)

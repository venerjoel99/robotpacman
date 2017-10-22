
#Top level class for simulating pacman game
#Steven Fontanella

class Game:

	GHOST_KILL_POINTS=0 #need to find this value
	BIG_DOT_COUNTER=30 #and this one, the amount of time a big dot lasts
	DOT_POINTS=1

	def __init__(self, numGhosts, width,height):
		self.pacman=Pacman() #initialize pacbot
		self.ghosts=[Ghost() for i in range(numGhosts)] #initialize ghosts

		self.maze=maze(width,height) #initialize maze
		self.points=0

		self.bigDotMode=False
		self.bigDotTimeRemaining=0

		for ghost in self.ghosts:
			ghost.setPosition(self.maze) # set starting positions, may have to split this up to assign different starting locations to each

	def nextStep(self):
		for ghost in self.ghosts:
			ghost.move(self.maze) #each ghost independently picks what direction it wants to move in
		self.pacman.move(self.maze) #^
		self.maze.checkDots(pacman) #check if a new dot has been passed over
		self.bigDotTimeRemaining-=1 #count down big dot duration

		if bigDotTimeRemaining<=0:
			self.bigDotMode=False
		#print(self.maze)
		return self.checkLoss() #return whether a loss has occurred so the simulation can stop

	def checkLoss(self):
		for ghost in self.ghosts:
			if isAdjacent(ghost.getPosition(),pacman.getPosition()) and not self.bigDotMode:
				return True
			elif ghost.getPosition()==pacman.getPosition() and self.bigDotMode:
				self.points+=GHOST_KILL_POINTS
				ghost.kill()

		return False

	def bigDotCollected(self):
		self.bigDotMode=True
		self.bigDotTimeRemaining=BIG_DOT_COUNTER #reset countdown clock for big dot


	def checkDots(self):
		if self.maze.hasPoint(pacman.getPosition()):
			self.points+=DOT_POINTS
			self.maze.removeDot(pacman.getPosition())

	def isAdjacent(point1,point2):
		return (point1[0]-point2[0])**2 + (point1[1]-point2[0])**2<=1

if __name__=="__main__":
	Game game=Game(5,10,10)
	gameOver=False


	while(not gameOver):
		game.nextStep()
		print(game.maze)


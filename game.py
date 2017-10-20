
#Top level class for simulating pacman game
#Steven Fontanella

class Game:

	def __init__(self, numGhosts, width,height):
		self.pacman=Pacman() #initialize pacbot
		self.ghosts=[Ghost() for i in range(numGhosts)] #initialize ghosts

		self.maze=maze(width,height) #initialize maze

		for ghost in self.ghosts:
			ghost.setPosition(self.maze) # set starting positions, may have to split this up to assign different starting locations to each

	def nextStep(self):
		for ghost in self.ghosts:
			ghost.move(self.maze) #each ghost independently picks what direction it wants to move in
		self.pacman.move(self.maze) #^
		self.maze.checkDots(pacman) #check if a new dot has been passed over
		#print(self.maze)
		return self.checkLoss() #return whether a loss has occurred so the simulation can stop

	def checkLoss(self):
		for ghost in self.ghosts:
			if ghost.getPosition()==pacman.getPosition():
				return True

		return False

if __name__=="__main__":
	Game game=Game(5,10,10)
	gameOver=False


	while(not gameOver):
		game.nextStep()
		print(game.maze)


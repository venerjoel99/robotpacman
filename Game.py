
#Top level class for simulating pacman game
#Steven Fontanella
from Pacman import Pacman
from Maze import Maze
from Ghost import Ghost



class Game:

	GHOST_KILL_POINTS_INITAL=200 #constant
	ghost_kill_points=200 #changes when multiple ghosts are killed in a row
	BIG_DOT_COUNTER=20
	DOT_POINTS=10
	BIG_DOT_POINTS=50
	NUM_GHOSTS=5

	def __init__(self, numGhosts, width,height):
		self.pacman=Pacman() #initialize pacbot
		self.ghosts=[Ghost() for i in range(NUM_GHOSTS)] #initialize ghosts

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
			ghost_kill_points=GHOST_KILL_POINTS_INITAL
		#print(self.maze)
		return self.checkLoss() #return whether a loss has occurred so the simulation can stop



	def checkLoss(self):
		for ghost in self.ghosts:
			if isAdjacent(ghost.getPosition(),pacman.getPosition()) and not self.bigDotMode:
				return True
			elif ghost.getPosition()==pacman.getPosition() and self.bigDotMode:
				self.points+=ghost_kill_points
				ghost.kill()
				ghost_kill_points*=2 #points awarded for each subsequent ghost killed are doubled until the time runs out

		return False

	def bigDotCollected(self):
		self.bigDotMode=True
		self.bigDotTimeRemaining=BIG_DOT_COUNTER #reset countdown clock for big dot
		self.points+=BIG_DOT_POINTS


	def checkDots(self):
		if self.maze.hasDot(pacman.getPosition()):
			self.points+=DOT_POINTS
			self.maze.removeDot(pacman.getPosition())

	def isAdjacent(point1,point2):
		return (point1[0]-point2[0])**2 + (point1[1]-point2[0])**2<=1

if __name__=="__main__":
	game=Game(5,10,10)
	gameOver=False


	while(not game.checkLoss()):
		game.nextStep()
		print(game.maze)


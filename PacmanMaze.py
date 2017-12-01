import Maze
import Tile

class PacmanMaze:

	def __init__(self,pacman,size=100):
		self.pacman=pacman
		self.arena=[[Node("Unknown") for i in range(size)] for j in range(size)]
		self.update()
		self.updateTile(self,maze,self.pacman.x,self.pacman.y)
	def update(self,maze): #update all adjacent tiles
		x,y=self.pacman.getPos()
		self.updateTile(maze,(x+1,y))
		self.updateTile(maze,(x,y+1))
		self.updateTile(maze,(x-1,y))
		self.updateTile(maze,(x,y-1))

		hee=self.arena[x][y]
		left=self.arena[x-1][y]
		right=self.arena[x+1][y]
		up=self.arena[x][y-1]
		down=self.arena[x][y+1]

		here.addConnection(left)
		here.addConnection(right)
		here.addConnection(up)
		here.addConnection(down)

		left.explore(maze)
		right.explore(maze)
		up.explore(maze)
		down.explore(maze)		

	def __str__(self):
		s=""
		for y in range(self.y):
			for x in range(self.x):
				s+=str(self.arena[x][y])
			s+="\n"

		return s

class Node(Tile):

	def __init__(self,x,y,type):
		super(type)
		self.up=None
		self.down=None
		self.left=None
		self.right=None
		self.position=(x,y)

	def addConnection(self,node):
		x1,y1=self.position
		x2,y2=node.position

		if x2>x1:
			self.right=node
			node.left=self
		elif x2<x1:
			self.left=node
			node.right=self
		elif y2>y1:
			self.down=node
			node.up=self
		elif y2<y1:
			self.up=node
			node.down=self

	def explore(self,maze):
		x,y=self.position

		self.type=maze[x][y].type





if __name__=="__main__":
	p=PacmanMaze(None)
	print(p)